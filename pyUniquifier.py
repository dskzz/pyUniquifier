""" Uniqifer - Generate a file with a UUID and load it when asked for UUID.  
      Designed to create a generic way to make sure each software user is unique.
      Fairly robust.  
"""

from classtools import AttrDisplay
import inspect
import uuid
from uuid import UUID
import sys
import os

class uniqifer (AttrDisplay):
      uuid_version_pref = (3, 5, 4, 1)
      default_filename = 'py-uniqifier-id'
      slash_type = '\\'
      full_loc = ''
      uuid_string = None
      uuid_version = 3
      verbose = False

      def __init__( self, path = None, filename = None, preff_version = 3, verbose = False ):
            if sys.platform.startswith('win'):
                  self.slash_type = '\\'
                  start_file_with_a_dot = ''
            else:
                 self.slash_type = '/' 
                 start_file_with_a_dot = '.'

            if filename is None:
                  filename = start_file_with_a_dot + self.default_filename

            if path is None:
                  path = self.get_script_dir( )

            if path[-1] != self.slash_type:
                  path += self.slash_type

            self.full_loc = path + filename

            if self.check_file_exists( self.full_loc ) is True:
                  self.load_existing_uuid( )
            else:
                  self.create_new_uuid( )

      def get_uuid( self ):
            if self.uuid_string is None:
                  load_existing_uuid( )
            else:
                  return str(self.uuid_string)

      def get_version( self ):
            return str(self.uuid_version)

      def create_new_uuid( self, preff_version = None ):
            if self.generate_uuid( preff_version ) is None:
                  return None
            else:
                  f = open( self.full_loc, "w")
                  f.write( str(self.uuid_string) +"\n")
                  f.write( str(self.uuid_version) +"\n" )
                  f.close( )

            return str(self.uuid_string)

      def load_existing_uuid( self ):
            f = open( self.full_loc, "r")
            lines = f.readlines()
            f.close( )

            if len(lines) != 2:
                  new_uuid = self.create_new_uuid()
                  if new_uuid is not None: 
                        return self.load_existing_uuid()
                  else:
                        self.out("Error failed to create a UUID", True)
                        return ""

            should_be_id = lines[0].rstrip("\n")
            should_be_version = lines[1].rstrip("\n")
            if self.check_valid_uuid( should_be_id, should_be_version ) is True:
                  self.uuid_string = should_be_id
                  self.uuid_version = should_be_version

            return str(self.uuid_string)

      def generate_uuid( self, preff_version = None ):
            i = 0
            if preff_version is not None and preff_version != 2:
                  self.uuid_version_pref  =   (preff_version, self.uuid_version_pref)


            while (1):
                  if i >= len( self.uuid_version_pref ):
                        print "Failed to provide a UUID"
                        self.uuid_string = None
                        self.uuid_version = None 
                        return ""

                  uuid_ver = self.uuid_version_pref[i]
                  uuid_str = self.create_uuid_by_version( uuid_ver )
                  
                  if uuid_str is not None and self.check_valid_uuid( uuid_str, uuid_ver ) is True:
                        self.uuid_string = uuid_str
                        self.uuid_version = uuid_ver 
                        return self.uuid_string
                  i += 1

      
      def create_uuid_by_version( self, version ):
            if version == 1:  
                  return uuid.uuid1()           # MAC and timestamp
            elif version == 2: 
                  return None
            elif version == 3:
                  return uuid.uuid3(uuid.NAMESPACE_DNS, 'python') #MD5
            elif version == 4:
                  return uuid.uuid4()           # random
            elif version == 5:
                  return uuid.uuid5(uuid.NAMESPACE_DNS, 'python') #SHA-1
            else:
                  return None

      def out( self, txt, force = False):
            if self.verbose is True or force is True:
                  print (txt)

      def verbose( self, turn_on = True ):
            self.verbose = turn_on

      def dump( self, force = False ):
             if self.verbose is True or force is True:
                  print ("UUID set; V: "+self.uuid_version +"; UUID: [" + self.uuid_string + "] File: " + self.full_loc )

      def check_valid_uuid( self, uuid_string, version = None ):
            #print "\nCheck valid - " + str(uuid_string) + " v " + str(version)
            if version is None:
                  version = self.uuid_version
            try:
                  uuid_test = str(uuid_string).replace('-','')
                  v= UUID( uuid_test, version=int(version) )
            except Exception as e:
                  self.out( "Error in validation", True )
                  self.out( e , True )
                  return False
            return True

      def check_file_exists( self, file ):
            if( os.path.isfile( file ) ):
                  return True
            else:
                  return False

      def get_script_dir(self, follow_symlinks=True):
            if getattr(sys, 'frozen', False): # py2exe, PyInstaller, cx_Freeze
                  path = os.path.abspath(sys.executable)
            else:
                  path = inspect.getabsfile(self.get_script_dir)
            
            if follow_symlinks:
                  path = os.path.realpath(path)
            
            return os.path.dirname(path)

if __name__ == '__main__':
      #     path = None, filename = None, verbose = False ):
      u = uniqifer( None, None, True )
      print u
      print u.get_uuid()
            
 #     print u.create_new_uuid(5) + " v: " +str(u.get_version())
#      print u.create_new_uuid(4)+ " v: " +str(u.get_version())
#     print u.create_new_uuid(3)+ " v: " +str(u.get_version())
#      print u.create_new_uuid(2)+ " v: " +str(u.get_version())
 #     print u.create_new_uuid(1)+ " v: " +str(u.get_version())


