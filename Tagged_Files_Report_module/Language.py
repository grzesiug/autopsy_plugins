# -*- coding: UTF-8 -*-
#
# Create by: Grzegorz Ginalski grzegorz.ginalski@o2.pl
#
# This is free and unencumbered software released into the public domain.
#
# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.
#
# In jurisdictions that recognize copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

from java.io import File
import os
import re
import codecs
from org.sleuthkit.autopsy.coreutils import Logger
from java.util.logging import Level
import inspect
import glob


class Language():
   
    def __init__(self):
        self._logger = Logger.getLogger("Language")	
        module_dir,tail = os.path.split(os.path.abspath(__file__))
        self.language_dir=os.path.join(module_dir,"language")
		

        self.dict={'LANGUAGE':'LANGUAGE'}

				
    def translate(self, keyword):	
        if keyword in self.dict:
            return self.dict.get(keyword)
        else:
            return keyword

    def log(self, level, msg):
        self._logger.logp(level, self.__class__.__name__, inspect.stack()[1][3], msg)	

    def setLanguageTo(self, language_name):
	
        self.dict.clear()	
        if language_name=="english_default":
            return		
        language_file = "lang_" + language_name + "_.txt"	
        lang_file_path=os.path.join(self.language_dir,language_file)
        try:		
            lang_file = codecs.open(lang_file_path,'r',"UTF-8")
            lines = list(lang_file)
            for line in lines:
                try:
		            #split wg ';' i pobranie textu pomiędzy znakami "" 
                    key = re.findall('".*"', line.split(';')[0])[0]
                    value = re.findall('".*"', line.split(';')[1])[0]
		    	    #usunięcie znaków "
                    key = key.replace('"','')
                    value =  value.replace('"','')
		    	    #dodanie wartości di dictionary
                    self.dict[key]=value
                except BaseException as e:
                    self.log(Level.INFO,str(e))				
            lang_file.close()
        except BaseException as e:
            self.log(Level.INFO,str(e))
	
    def getLanguages(self):
        try:
            lang_files = ["english_default"]
            for file in glob.glob(os.path.join(self.language_dir,"lang_*_.txt")):
                file_name= os.path.basename(file)
                language = re.findall('_.*_',file_name)[0]
                language = language.replace('_','')			
                lang_files.append(language) 			
            return lang_files
        except BaseException as e:
            self.log(Level.INFO,str(e))