from ckanext.harvest.model import HarvestObject
from ckan.plugins.core import SingletonPlugin, implements
from ckanext.harvest.interfaces import IHarvester
from ckanext.harvest.harvesters.base import HarvesterBase
from ckanext.harvest.harvesters.ckanharvester import CKANHarvester
import json
import logging
log = logging.getLogger(__name__)

#class RostockTestHarvester(HarvesterBase, SingletonPlugin):
class RostockTestHarvester(CKANHarvester, SingletonPlugin):
    implements(IHarvester)
    
    
    def info(self):
        return {'name':        'test-rostock',
                'title':       'Rostock Test Harvester',
                'description': 'A CKAN Harvester for Rostock solving data '
                'compatibility problems.'}



    def gather_stage(self, harvest_job):

        """Retrieve datasets"""
        
        log.debug('In RostockTestHarvester gather_stage (%s)' % harvest_job.source.url)
        package_ids = []
        self._set_config(None)

        base_url = harvest_job.source.url.rstrip('/')
        package_list_url = base_url + '/api/rest/package'
        content = self._get_content(package_list_url)
        
        package_ids = json.loads(content)

        try:
            object_ids = []
            if len(package_ids):
                for package_id in package_ids:                                      
                    obj = HarvestObject(guid = package_id, job = harvest_job)
                    obj.save()
                    object_ids.append(obj.id)
                    log.info('Got ID from source: %s' %package_id)
                return object_ids

            else:
               self._save_gather_error('No packages received for URL: %s' % url,
                       harvest_job)
               return None
        except Exception, e:
            self._save_gather_error('%r'%e.message,harvest_job)
        
        

            
    def fetch_stage(self,harvest_object):
        log.debug('In RostockTestHarvester fetch_stage')
        self._set_config(None)
       
        # Get contents
        package_get_url = ''
        try:    
            base_url = harvest_object.source.url.rstrip('/')
      
            package_get_url = base_url + '/api/rest/package/' + harvest_object.guid
            harvest_object.content = self._get_content(package_get_url)
            harvest_object.save()

        except Exception,e:
            self._save_object_error('Unable to get content for package: %s: %r' % \
                                        (package_get_url, e),harvest_object)
            return None
        return True



    PORTAL = 'http://www.opendata-hro.de'

    def amend_package(self, package):
        portal = 'http://www.opendata-hro.de'
        package['extras']['metadata_original_portal'] = portal
        package['name'] = package['name'] + '-hro'
        
        for resource in package['resources']:
                resource['format'] = resource['format'].lower()


    def import_stage(self, harvest_object):
        package_dict = json.loads(harvest_object.content)
        try:
            self.amend_package(package_dict)
        except ValueError, e:
            self._save_object_error(str(e), harvest_object)
            log.error('Rostock: ' + str(e))
            return
        harvest_object.content = json.dumps(package_dict)
        super(RostockTestHarvester, self).import_stage(harvest_object)