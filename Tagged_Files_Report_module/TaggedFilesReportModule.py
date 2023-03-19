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


# Meta Data html report module for Autopsy. 

# Create Sept 2019
#
# Version 1.0 - Initial creation - Sept 2019
#

from __future__ import division
import os
import inspect
import datetime
import sys
import codecs
reload(sys)
sys.setdefaultencoding('utf8')
from java.lang import System
from java.util.logging import Level
from org.sleuthkit.autopsy.casemodule import Case
from org.sleuthkit.autopsy.coreutils import Version
from org.sleuthkit.autopsy.coreutils import Logger
from org.sleuthkit.autopsy.report import GeneralReportModuleAdapter
from org.sleuthkit.autopsy.report.ReportProgressPanel import ReportStatus
from distutils.dir_util import copy_tree
from org.sleuthkit.autopsy.datamodel import ContentUtils
from org.sleuthkit.datamodel import SleuthkitCase
from java.io import File
from org.sleuthkit.datamodel import  AbstractFile;
from org.sleuthkit.datamodel import  Content;
from org.sleuthkit.datamodel import  ContentTag;
from org.sleuthkit.datamodel import  TagName;
from org.sleuthkit.datamodel import  TskCoreException;

from javax.swing import JCheckBox
from javax.swing import JButton
from javax.swing import ButtonGroup
from javax.swing import JTextField
from javax.swing import JLabel
from javax.swing import JList
from java.awt import GridLayout
from java.awt import GridBagLayout
from java.awt import GridBagConstraints
from java.awt.event import ItemEvent
from javax.swing import JPanel
from javax.swing import JScrollPane
from javax.swing import JFileChooser
from javax.swing import JComboBox
from javax.swing.filechooser import FileNameExtensionFilter
import time
import re




class TagHtmlReportModule(GeneralReportModuleAdapter):
    

    def __init__(self):
        self.tags_selected = []
        self.moduleName = "Tagged Files Report" 
        self._logger = Logger.getLogger(self.moduleName)
        self.charEncoding="UTF-8"

        self.module_dir, tail = os.path.split(os.path.abspath(__file__))
        self.lang = Language()	
        self.report_file_name=self.lang.translate("Report.html")

    def log(self, level, msg):
        self._logger.logp(level, self.__class__.__name__, inspect.stack()[1][3], msg)

    def getName(self):	
        return self.moduleName

    def getDescription(self):
        return self.moduleName

    def getRelativeFilePath(self):
        return self.report_file_name

    def getConfigurationPanel(self):
        self.artifact_list = []
        self.panel0 = JPanel()

        self.rbgPanel0 = ButtonGroup() 
        self.gbPanel0 = GridBagLayout() 
        self.gbcPanel0 = GridBagConstraints() 
        self.panel0.setLayout( self.gbPanel0 ) 

        self.Label_0 = JLabel("Number of Object to Display per page")
        self.gbcPanel0.gridx = 1 
        self.gbcPanel0.gridy = 1 
        self.gbcPanel0.gridwidth = 1 
        self.gbcPanel0.gridheight = 1 
        self.gbcPanel0.fill = GridBagConstraints.BOTH 
        self.gbcPanel0.weightx = 1 
        self.gbcPanel0.weighty = 0 
        self.gbcPanel0.anchor = GridBagConstraints.NORTH 
        self.gbPanel0.setConstraints( self.Label_0, self.gbcPanel0 ) 
        self.panel0.add( self.Label_0 ) 

        self.Num_Of_Objs_Per_Page_TF = JTextField(5) 
        self.Num_Of_Objs_Per_Page_TF.setEnabled(True)
        self.Num_Of_Objs_Per_Page_TF.setText("10")
        self.gbcPanel0.gridx = 3 
        self.gbcPanel0.gridy = 1 
        self.gbcPanel0.gridwidth = 1 
        self.gbcPanel0.gridheight = 1 
        self.gbcPanel0.fill = GridBagConstraints.BOTH 
        self.gbcPanel0.weightx = 1 
        self.gbcPanel0.weighty = 0 
        self.gbcPanel0.anchor = GridBagConstraints.NORTH 
        self.gbPanel0.setConstraints( self.Num_Of_Objs_Per_Page_TF, self.gbcPanel0 ) 
        self.panel0.add( self.Num_Of_Objs_Per_Page_TF ) 


        self.Label_1 = JLabel("Report language")
        self.gbcPanel0.gridx = 1 
        self.gbcPanel0.gridy = 5 
        self.gbcPanel0.gridwidth = 1 
        self.gbcPanel0.gridheight = 1 
        self.gbcPanel0.fill = GridBagConstraints.BOTH 
        self.gbcPanel0.weightx = 1 
        self.gbcPanel0.weighty = 0 
        self.gbcPanel0.anchor = GridBagConstraints.NORTH 
        self.gbPanel0.setConstraints( self.Label_1, self.gbcPanel0 ) 
        self.panel0.add( self.Label_1 ) 



        langList = self.lang.getLanguages()	
        self.Language_Combobox = JComboBox(langList) 
        self.Language_Combobox.setEnabled(True)	
        self.Language_Combobox.itemStateChanged = self.eventListener		
        self.gbcPanel0.gridx = 3 
        self.gbcPanel0.gridy = 5 
        self.gbcPanel0.gridwidth = 1 
        self.gbcPanel0.gridheight = 1 
        self.gbcPanel0.fill = GridBagConstraints.BOTH 
        self.gbcPanel0.weightx = 1 
        self.gbcPanel0.weighty = 0 
        self.gbcPanel0.anchor = GridBagConstraints.NORTH 
        self.gbPanel0.setConstraints( self.Language_Combobox, self.gbcPanel0 ) 
        self.panel0.add( self.Language_Combobox) 


        self.Label_2 = JLabel("Report Number To Appear on Case Info")
        self.gbcPanel0.gridx = 1 
        self.gbcPanel0.gridy = 7 
        self.gbcPanel0.gridwidth = 1 
        self.gbcPanel0.gridheight = 1 
        self.gbcPanel0.fill = GridBagConstraints.BOTH 
        self.gbcPanel0.weightx = 1 
        self.gbcPanel0.weighty = 0 
        self.gbcPanel0.anchor = GridBagConstraints.NORTH 
        self.gbPanel0.setConstraints( self.Label_2, self.gbcPanel0 ) 
        self.panel0.add( self.Label_2 ) 

        self.Report_Number_TF = JTextField(30) 
        self.Report_Number_TF.setEnabled(True)
        self.Report_Number_TF.setText(Case.getCurrentCase().getNumber())
        self.gbcPanel0.gridx = 3 
        self.gbcPanel0.gridy = 7 
        self.gbcPanel0.gridwidth = 1 
        self.gbcPanel0.gridheight = 1 
        self.gbcPanel0.fill = GridBagConstraints.BOTH 
        self.gbcPanel0.weightx = 1 
        self.gbcPanel0.weighty = 0 
        self.gbcPanel0.anchor = GridBagConstraints.NORTH 
        self.gbPanel0.setConstraints( self.Report_Number_TF, self.gbcPanel0 ) 
        self.panel0.add( self.Report_Number_TF ) 

        self.Label_3 = JLabel("Examiner(s) To Appear on Case Info")
        self.gbcPanel0.gridx = 1 
        self.gbcPanel0.gridy = 9 
        self.gbcPanel0.gridwidth = 1 
        self.gbcPanel0.gridheight = 1 
        self.gbcPanel0.fill = GridBagConstraints.BOTH 
        self.gbcPanel0.weightx = 1 
        self.gbcPanel0.weighty = 0 
        self.gbcPanel0.anchor = GridBagConstraints.NORTH 
        self.gbPanel0.setConstraints( self.Label_3, self.gbcPanel0 ) 
        self.panel0.add( self.Label_3 ) 

        self.Examiners_TF = JTextField(30) 
        self.Examiners_TF.setEnabled(True)
        self.Examiners_TF.setText(Case.getCurrentCase().getExaminer())
        self.gbcPanel0.gridx = 3 
        self.gbcPanel0.gridy = 9
        self.gbcPanel0.gridwidth = 1 
        self.gbcPanel0.gridheight = 1 
        self.gbcPanel0.fill = GridBagConstraints.BOTH 
        self.gbcPanel0.weightx = 1 
        self.gbcPanel0.weighty = 0 
        self.gbcPanel0.anchor = GridBagConstraints.NORTH 
        self.gbPanel0.setConstraints( self.Examiners_TF, self.gbcPanel0 ) 
        self.panel0.add( self.Examiners_TF ) 

        self.Label_4 = JLabel("Description To Appear on Case Info")
        self.gbcPanel0.gridx = 1 
        self.gbcPanel0.gridy = 11 
        self.gbcPanel0.gridwidth = 1 
        self.gbcPanel0.gridheight = 1 
        self.gbcPanel0.fill = GridBagConstraints.BOTH 
        self.gbcPanel0.weightx = 1 
        self.gbcPanel0.weighty = 0 
        self.gbcPanel0.anchor = GridBagConstraints.NORTH 
        self.gbPanel0.setConstraints( self.Label_4, self.gbcPanel0 ) 
        self.panel0.add( self.Label_4 ) 

        self.Description_TF = JTextField(30) 
        self.Description_TF.setEnabled(True)
        self.gbcPanel0.gridx = 3 
        self.gbcPanel0.gridy = 11 
        self.gbcPanel0.gridwidth = 1 
        self.gbcPanel0.gridheight = 1 
        self.gbcPanel0.fill = GridBagConstraints.BOTH 
        self.gbcPanel0.weightx = 1 
        self.gbcPanel0.weighty = 0 
        self.gbcPanel0.anchor = GridBagConstraints.NORTH 
        self.gbPanel0.setConstraints( self.Description_TF, self.gbcPanel0 ) 
        self.panel0.add( self.Description_TF ) 




        self.Blank_5 = JLabel( "Sort files by:") 
        self.Blank_5.setEnabled(True)
        self.gbcPanel0.gridx = 1 
        self.gbcPanel0.gridy = 21
        self.gbcPanel0.gridwidth = 1 
        self.gbcPanel0.gridheight = 1 
        self.gbcPanel0.fill = GridBagConstraints.BOTH 
        self.gbcPanel0.weightx = 1 
        self.gbcPanel0.weighty = 0 
        self.gbcPanel0.anchor = GridBagConstraints.NORTH 
        self.gbPanel0.setConstraints( self.Blank_5, self.gbcPanel0 ) 
        self.panel0.add( self.Blank_5 ) 
		
        sortItems = [ 'Date Modified' ,'Date Created','Date Accessed', 'File Path', 'File Name','File Size', 'MD5 Hash','SHA256 Hash', 'MIME Type' ]	
        self.SortBy_Combobox = JComboBox(sortItems) 
        self.SortBy_Combobox.setEnabled(True)
        self.gbcPanel0.gridx = 3 
        self.gbcPanel0.gridy = 21 
        self.gbcPanel0.gridwidth = 1 
        self.gbcPanel0.gridheight = 1 
        self.gbcPanel0.fill = GridBagConstraints.BOTH 
        self.gbcPanel0.weightx = 1 
        self.gbcPanel0.weighty = 0 
        self.gbcPanel0.anchor = GridBagConstraints.NORTH 
        self.gbPanel0.setConstraints( self.SortBy_Combobox, self.gbcPanel0 ) 
        self.panel0.add( self.SortBy_Combobox) 

        self.Label_6 = JLabel( "Select which data source(s) to include:") 
        self.Label_6.setEnabled(True)
        self.gbcPanel0.gridx = 3 
        self.gbcPanel0.gridy = 22
        self.gbcPanel0.gridwidth = 1 
        self.gbcPanel0.gridheight = 1 
        self.gbcPanel0.fill = GridBagConstraints.BOTH
        self.gbcPanel0.weightx = 1 
        self.gbcPanel0.weighty = 0 
        self.gbcPanel0.anchor = GridBagConstraints.NORTH 
        self.gbPanel0.setConstraints( self.Label_6, self.gbcPanel0 ) 
        self.panel0.add( self.Label_6 ) 
		
        data_source_list = self.get_data_sources()
        self.List_Box_Sources = JList( data_source_list, valueChanged=self.onchange_sb)
        self.List_Box_Sources.setVisibleRowCount( 3 ) 
        self.scpList_Box_Sources = JScrollPane( self.List_Box_Sources ) 
        self.gbcPanel0.gridx = 3 
        self.gbcPanel0.gridy = 23 
        self.gbcPanel0.gridwidth = 1 
        self.gbcPanel0.gridheight = 1 
        self.gbcPanel0.fill = GridBagConstraints.BOTH 
        self.gbcPanel0.weightx = 1 
        self.gbcPanel0.weighty = 1 
        self.gbcPanel0.anchor = GridBagConstraints.NORTH 
        self.gbPanel0.setConstraints( self.scpList_Box_Sources, self.gbcPanel0 )
        self.List_Box_Sources.setSelectionInterval(0,self.List_Box_Sources.getModel().getSize() - 1)
        self.panel0.add( self.scpList_Box_Sources ) 

        self.Label_5 = JLabel( "Tags to Select for Report:") 
        self.Label_5.setEnabled(True)
        self.gbcPanel0.gridx = 1 
        self.gbcPanel0.gridy = 22
        self.gbcPanel0.gridwidth = 1 
        self.gbcPanel0.gridheight = 1 
        self.gbcPanel0.fill = GridBagConstraints.BOTH 
        self.gbcPanel0.weightx = 1 
        self.gbcPanel0.weighty = 0 
        self.gbcPanel0.anchor = GridBagConstraints.NORTH 
        self.gbPanel0.setConstraints( self.Label_5, self.gbcPanel0 ) 
        self.panel0.add( self.Label_5 ) 

        self.tag_list=self.find_tags()
        self.List_Box_LB = JList( self.tag_list, valueChanged=self.onchange_lb)
        self.List_Box_LB.setVisibleRowCount( 3 ) 
        self.scpList_Box_LB = JScrollPane( self.List_Box_LB ) 
        self.gbcPanel0.gridx = 1 
        self.gbcPanel0.gridy = 23 
        self.gbcPanel0.gridwidth = 1 
        self.gbcPanel0.gridheight = 1 
        self.gbcPanel0.fill = GridBagConstraints.BOTH 
        self.gbcPanel0.weightx = 1 
        self.gbcPanel0.weighty = 1 
        self.gbcPanel0.anchor = GridBagConstraints.NORTH 
        self.gbPanel0.setConstraints( self.scpList_Box_LB, self.gbcPanel0 ) 
        self.panel0.add( self.scpList_Box_LB ) 
        
        return self.panel0
        
    def generateReport(self, baseReportDir, progressBar):


		
		# Get tag from selected data sources
        tags = Case.getCurrentCase().getServices().getTagsManager().getAllContentTags()
        self.data_source_tags=[]
        for tag in tags:
            for source in self.data_source_selected:
                if source.Id==tag.getContent().getDataSource().getId():
                   self.data_source_tags.append(tag)
        if len(self.data_source_tags)==0:	
            progressBar.complete(ReportStatus.ERROR)
            progressBar.updateStatusLabel("No tags to proceed!")			
            return
			
        no_empty_tags_selected=[]
        for sel_tag in self.tags_selected:
            tags_to_process = []
            for tag in self.data_source_tags:
                if tag.getName().getDisplayName() == sel_tag:
					       tags_to_process.append(tag)
			#jeśli w danej grupie wystepują tagi to dodaje do listy			   
            if len(tags_to_process)>0:
                no_empty_tags_selected.append(sel_tag)
                self.log(Level.INFO, "this is a content tags ==> " + str(sel_tag) + " <==")				
        # do zaznoczonych tagów podstawiamy tylko te które maja elementy dla zaznaczonych data source	
        self.tags_selected=no_empty_tags_selected
		
        self.lang.setLanguageTo(self.Language_Combobox.getSelectedItem())
        self.report_file_name=self.lang.translate("Report.html")
        progressBar.setIndeterminate(False)
        progressBar.start()
		
        # Set status bar for number of tags
        progressBar.setMaximumProgress(len(self.tags_selected)+2)

        
        # Get and create the report directories
        head, tail = os.path.split(os.path.abspath(__file__)) 
        copy_resources_dir = os.path.join(head, "res")

        try:
            report_dir = os.path.join(baseReportDir.getReportDirectoryPath(), self.lang.translate("Report"))
            os.mkdir(report_dir)
        except:
            self.log(Level.INFO, "Could not create base report dir")
            
        try:
            report_files_dir = os.path.join(report_dir, self.lang.translate("Tagged_Files"))
            os.mkdir(report_files_dir)
        except:
            self.log(Level.INFO, "Could not create report_files directory")
			
          
         
        try:
            report_resources_dir = os.path.join(report_dir , "res")
            os.mkdir(report_resources_dir)
        except:
            self.log(Level.INFO, "Could not create report_res directory")
			
			
            
        # Copy the Resource directory to the report directory
        try:
            head, tail = os.path.split(os.path.abspath(__file__)) 
            copy_resources_dir = os.path.join(head, "res")
            copy_tree(copy_resources_dir, report_resources_dir)
        except:
            self.log(Level.INFO, "Could Not copy resources directory")

         
        # Create the index page        
        self.create_index_file(baseReportDir.getReportDirectoryPath())
         
        # Create The information page
        try:
           self.create_info_page(report_resources_dir)
        except:
            self.log(Level.INFO, "Could not write to info_page")
        # Create the Menu page.
        self.create_menu_file(report_resources_dir)
         
        # Get all Content
        tags = self.data_source_tags
        tag_number = 1
        no_empty_tags_selected=[]
        for sel_tag in self.tags_selected:
            tags_to_process = []
            for tag in tags:
                if tag.getName().getDisplayName() == sel_tag:
					       tags_to_process.append(tag)	
            #self.log(Level.INFO, "this is a content tags ==> " + str(sel_tag) + " <==")
            progressBar.updateStatusLabel("Process tag " + sel_tag)
            sorted_tag=self.sort_tags(tags_to_process,self.SortBy_Combobox.getSelectedItem())
            try:
                if len(sorted_tag)>0:        
                   self.process_thru_tags(report_resources_dir,sorted_tag , tag_number, sel_tag, report_files_dir)
            except BaseException as e:	
                self.log(Level.INFO, str(e) )
            progressBar.increment()	
            tag_number = tag_number + 1
			

			
		#Create help file	
        self.create_help_page(report_resources_dir)        
        # Increment since we are done with step #1
        progressBar.increment()

        fileName = os.path.join(baseReportDir.getReportDirectoryPath(), self.report_file_name)

        # Add the report to the Case, so it is shown in the tree
        try:		
             Case.getCurrentCase().addReport(fileName, self.moduleName, self.moduleName)
        except:
            self.log(Level.INFO, "Could not add report to case")
        progressBar.increment()

        # Call this with ERROR if report was not generated
        progressBar.complete(ReportStatus.COMPLETE)

    def process_thru_tags(self, report_dir, tags_to_process, book_mark_number, tag_name, report_files_dir):
	
        
        self.create_taged_files_folder(report_files_dir,self.standardize_folder_name(self.lang.translate(tag_name)))        	
        page_number = 1
        current_page_number = 1
        num_of_tags_per_page = int(str(self.Num_Of_Objs_Per_Page_TF.getText()))
        total_pages = int(len(tags_to_process))//num_of_tags_per_page
        if (int(len(tags_to_process)) % num_of_tags_per_page) <> 0:
            total_pages = total_pages + 1
        page_file_name = os.path.join(report_dir, self.lang.translate("Bookmark") + str(book_mark_number) + self.lang.translate("Page")  + str(page_number) + ".html")
        page_file = open(page_file_name, 'w')
        self.create_page_header(page_file, len(tags_to_process), tag_name, total_pages, page_number,self.lang.translate("Bookmark") + str(book_mark_number) + self.lang.translate("Page"),report_dir,num_of_tags_per_page)        
        tag_number = 1
        total_tag_number = 1
        for tag in tags_to_process:
            if tag_number > num_of_tags_per_page:
                tag_number = 1
                page_number = page_number + 1
                page_file_name = os.path.join(report_dir, self.lang.translate("Bookmark") + str(book_mark_number) + self.lang.translate("Page") + str(page_number) + ".html")
                self.create_page_footer(page_file, total_pages, current_page_number, self.lang.translate("Bookmark") + str(book_mark_number) + self.lang.translate("Page"),report_dir)
                page_file.close()
                #page_file_name = os.path.join(report_dir, self.lang.translate("Bookmark") + str(tag_number) + self.lang.translate("Page")+"1.html")
                page_file = open(page_file_name, 'w')
                self.create_page_header(page_file, len(tags_to_process), tag_name,total_pages, page_number,self.lang.translate("Bookmark") + str(book_mark_number) + self.lang.translate("Page"),report_dir,num_of_tags_per_page),
                current_page_number = current_page_number + 1
            self.create_page_data(page_file, tag, total_tag_number,report_dir, report_files_dir,tag_name)
            tag_number = tag_number + 1
            total_tag_number = total_tag_number + 1
        self.create_page_footer(page_file, total_pages, current_page_number, self.lang.translate("Bookmark") + str(book_mark_number) + self.lang.translate("Page"),report_dir)
        page_file.close()
    

    def create_page_footer(self, page_file, total_pages, current_page, page_file_name,report_dir):
	
        try:  
            		
            footerPath = os.path.join(self.module_dir,"html", "footer.html").encode(self.charEncoding)           
            footerFile = open(footerPath, 'r')            
            footerText = footerFile.read()           
            footerText = footerText.replace('*current_page*', str(current_page))
            footerText = footerText.replace('*total_pages*', str(total_pages))
            nextBookmarkFileName = page_file_name + str(current_page + 1) + ".html"
            prevBookmarkFileName = page_file_name + str(current_page - 1) + ".html"
            

            if  current_page == 1:
                    prevBookmarkFileName = ''
            if  current_page == total_pages:
                    nextBookmarkFileName = ''
					
            footerText = footerText.replace('*bookmark_prev_file*', prevBookmarkFileName)
            footerText = footerText.replace('*bookmark_next_file*', nextBookmarkFileName)
            #labels        
            footerText = footerText.replace('*lb_print*', self.lang.translate("Print") )
            footerText = footerText.replace('*lb_previous_page*', self.lang.translate("Previous page") )
            footerText = footerText.replace('*lb_next_page*', self.lang.translate("next page") )
                
			#dodaanie przycisków stron	
            buttons = self.create_page_buttons(page_file_name, current_page,total_pages)           				
            footerText = footerText.replace('*buttons*', buttons)				

            page_file.write(footerText)
        except BaseException as e:		
            self.log(Level.INFO, str(e))

    def create_page_data(self, page_file, tag, tag_number,report_dir, report_files_dir, tag_name):
        try:
		
		
            tag_content = tag.getContent()
            file_name = tag_content.getName()
            tag_folder_name =self.standardize_folder_name(self.lang.translate(tag_name))
            new_extension=''
            originalFilePath = tag_content.getUniquePath()
            index = str(tag_number)
            size = tag_content.getSize()
            obj_id=tag_content.getId()
            
            exif_dataPath = os.path.join(self.module_dir,"html", 'exif_data.html').encode(self.charEncoding)                 			                     
            exif_dataFile = open(exif_dataPath, 'r')               
            exif_dataText = exif_dataFile.read()
			
            gps_dataPath = os.path.join(self.module_dir,"html", 'gps_data.html').encode(self.charEncoding)                 			                     
            gps_dataFile = open(gps_dataPath, 'r')               
            gps_dataText = gps_dataFile.read()
            exif=''			
			
            if size<1024:
               strSize=str(size) + ' B'
            elif size<1048576:
                 strSize = str('{0:.2f}'.format(size/1024)) + ' KB'
            else:
                 strSize = str('{0:.2f}'.format((size/1048576))) + ' MB'            
            Created    = tag_content.getCrtimeAsDate()    
            Modified = tag_content.getMtimeAsDate()
            Accessed = tag_content.getAtimeAsDate()
            MimeType = str(tag_content.getMIMEType())
			
            if 	tag_content.getMd5Hash()==None:		                
                MD5 =   self.lang.translate("not calculated")
            else:
                MD5 =   str(tag_content.getMd5Hash())	

            if 	tag_content.getSha256Hash()==None:		                
                SHA256 =   self.lang.translate("not calculated")
            else:
                SHA256 =   str(tag_content.getSha256Hash())				

            if (tag_content.exists() and "$CarvedFiles/" not in originalFilePath):
                Deleted = self.lang.translate("No")
            else:
                Deleted = self.lang.translate("Yes")
            src = ""

			#Jeśli plik video,image, text to wybieramy kod html z pliku bookmark.html
            bookmark_file="bookmark.html"			
			
            htmlVideoMime=['video/mp4','video/webm','video/quicktime','video/ogg','video/x-m4v']
            htmlAudioMime=['audio/mp4','audio/mpeg','audio/vnd.wave','audio/vorbis','audio/x-flac']			

			#zmienna przechowuje typ elementu HTML podstawianego do pliku bookmatk.html
            tagType='img'
            style = 'style="max-width: 100%; max-height: 62vh; min-height: 30vh; "'
            fileType=""
			#przechowuje code dla plików wideo określający czas podglądu np #t=0.5
            previewTime=''
			#Plik video
            if ("video/" in MimeType):
			    #sprawdzenie czy plik video jest na liście obsługiwanych plików video w html
               	if MimeType in htmlVideoMime:				
                    tagType='video controls'
                    previewTime = '#t=0.5'
                else:
                    src ="video.jpg"
            else:		
                if ("text/" in MimeType):
                    tagType='iframe' 
                    fileType='type="text/plain"'			
                    style='style="width: 100%; height: 64vh; "'
					#zmiana roszerzenia na txt jeśli jest inne
                    if self.get_extension(file_name)!='.txt':
                        new_extension='.txt'					
                else:
                    if ("audio/" in MimeType):
			            #sprawdzenie czy plik audio jest na liście obsługiwanych plików video w html
                        if MimeType in htmlAudioMime:				
                           tagType='audio controls' 
                           fileType='type="'+MimeType+'"'			
                           style='style="width: 100%; height: 20vh; padding: 20px;"'  					
                        else:
                            src ="audio.jpg"
                    else:
                        if ("image/" in MimeType):					
                            result = self.find_result(obj_id,16,'TSK_DEVICE_MAKE')
                            								
                            if len(result)>0:
                                for row in result:							
                                    display_name=row[0]						
                                    value=row[1]									
                                    if display_name=="Date Created":
                                        utc_time = time.gmtime(int(value))									
                                        value=time.strftime("%Y-%m-%d %H:%M:%S+ 00:00 (UTC)", utc_time)									
                                    exif_dataText=exif_dataText.replace('*'+display_name+'*',value)                           		
                                    gps_dataText=gps_dataText.replace('*'+display_name+'*',value) 	
                                exif =exif_dataText			

            #jeśli jest szerokość geo to dodaje wiersz z danymi gps
            if '*Latitude*' not in gps_dataText:
                exif+=gps_dataText			
			
			#Jeśli plik inny niż video,image,audio, text to wybieramy kod html z pliku bookmark_no_media.html
            if not("video/" in MimeType or "image/" in MimeType or "text/" in MimeType or "audio/" in MimeType):			
                #bookmark_file= "bookmark.html"
                bookmark_file= "bookmark_no_media.html"                
				# dla plików video, audio, text , image sprawdzamy rozszerzenie,
				# jeśli nie ma to dodajemy do nazwy esportowanego pliku
            else:				
                new_extension="."+ self.get_valid_file_ext(file_name, MimeType)
				#remove "." if there is no need to chenge extention 
                if (len(new_extension)==1): 
				    new_extension=""

						   
            exported_file_mame= self.standardize_folder_name(str(obj_id) + "-" + tag_content.getName()+new_extension)
            extractPath = os.path.join(report_files_dir,tag_folder_name,exported_file_mame)            
            #save selected file in report folder
            ContentUtils.writeToFile(tag_content, File(extractPath))            
            Exported = os.path.join(self.lang.translate("Tagged_Files") ,tag_folder_name, exported_file_mame)
            if src=="":
               src = "..\\"+Exported
			
            bookmarkPath = os.path.join(self.module_dir,"html", bookmark_file).encode(self.charEncoding)                 			                     
            bookmarkFile = open(bookmarkPath, 'r')               
            bookmarkText = bookmarkFile.read()
			
            bookmarkText = bookmarkText.replace('*exif*',exif)  			
            bookmarkText = bookmarkText.replace('*previewTime*',previewTime)
            bookmarkText = bookmarkText.replace('*style*',style)
            bookmarkText = bookmarkText.replace('*fileType*',fileType)
            bookmarkText = bookmarkText.replace('*style*',style)
            bookmarkText = bookmarkText.replace('*tagType*',tagType)
            bookmarkText = bookmarkText.replace('*extractPath*',"..\\"+Exported) 
            bookmarkText = bookmarkText.replace('*src*',src)             
            bookmarkText = bookmarkText.replace('*Exported*',self.lang.translate("Report")+"\\"+Exported)             
            bookmarkText = bookmarkText.replace('*originalFilePath*',originalFilePath)    
            bookmarkText = bookmarkText.replace('*MD5*',MD5)     
            bookmarkText = bookmarkText.replace('*SHA256*',SHA256) 			
            bookmarkText = bookmarkText.replace('*index*',index)                
            bookmarkText = bookmarkText.replace('*size*',strSize)    
            bookmarkText = bookmarkText.replace('*MimeType*',MimeType)
            bookmarkText = bookmarkText.replace('*Created*',str(Created))
            bookmarkText = bookmarkText.replace('*filename*',file_name)
            bookmarkText = bookmarkText.replace('*Modified*',str(Modified))            
            bookmarkText = bookmarkText.replace('*Accessed*',str(Accessed))
            bookmarkText = bookmarkText.replace('*Deleted*',str(Deleted))

			
			#labels
            bookmarkText = bookmarkText.replace('*lb_file_size*',self.lang.translate("File size"))
            bookmarkText = bookmarkText.replace('*lb_mime_type*',self.lang.translate("MIME Type"))
            bookmarkText = bookmarkText.replace('*lb_deleted*',self.lang.translate("Deleted"))
            bookmarkText = bookmarkText.replace('*lb_date*',self.lang.translate("Date"))	
            bookmarkText = bookmarkText.replace('*lb_date_created*',self.lang.translate("Date Created"))	
            bookmarkText = bookmarkText.replace('*lb_date_modified*',self.lang.translate("Date Modified"))	
            bookmarkText = bookmarkText.replace('*lb_date_accessed*',self.lang.translate("Date Accessed"	))	
            bookmarkText = bookmarkText.replace('*lb_exported_as*',self.lang.translate("Exported as:"))	
            bookmarkText = bookmarkText.replace('*lb_checksumSuma*',self.lang.translate("Checksum"))		
            bookmarkText = bookmarkText.replace('*lb_exif_metadata*',self.lang.translate("Exif Metadata"))	
            bookmarkText = bookmarkText.replace('*lb_generation_date*',self.lang.translate("Generation Date"))	
            bookmarkText = bookmarkText.replace('*lb_device_make*',self.lang.translate("Device Make"))	
            bookmarkText = bookmarkText.replace('*lb_device_model*',self.lang.translate("Device Model"))	
            bookmarkText = bookmarkText.replace('*lb_gps_position*',self.lang.translate("GPS Position"))	
            bookmarkText = bookmarkText.replace('*lb_google_maps*',self.lang.translate("Google Maps"))	
            bookmarkText = bookmarkText.replace('*lb_latitude*',self.lang.translate("Latitude"))	
            bookmarkText = bookmarkText.replace('*lb_longitude*',self.lang.translate("Longitude"))	
            bookmarkText = bookmarkText.replace('*lb_altitude*',self.lang.translate("Altitude"))				
   
			#replacing text between ** sighns
            bookmarkText = re.sub("\*.*\*","---",bookmarkText)
            			
            page_file.write(bookmarkText)      
        except BaseException as e:		
            self.log(Level.INFO, str(e))
            
    def create_page_header(self, page_file, number_of_tags, tag_name, total_pages,current_page, page_file_name,report_dir,num_of_tags_per_page):

        try:
              		
            headerPath = os.path.join(self.module_dir,"html", "header.html").encode(self.charEncoding)
            
            headerFile = open(headerPath, 'r')           
            headerText = headerFile.read()
            sorted_by=self.SortBy_Combobox.getSelectedItem()			
            skCase = Case.getCurrentCase()
			
            fileIndexStart = (num_of_tags_per_page*current_page) - num_of_tags_per_page +1
            fileIndexEnd = (num_of_tags_per_page*current_page)
            if fileIndexEnd>number_of_tags:
               fileIndexEnd=number_of_tags
            autopsy_version=Version.getVersion()   
            
            headerText = headerText.replace('*sorted_by*',self.lang.translate("Files sorted by *sorted_by* in ascending order."))
            headerText = headerText.replace('*sorted_by*',self.lang.translate(sorted_by))			
            headerText = headerText.replace('*case_info*',self.lang.translate("Case Information"))

            headerText = headerText.replace('*title*',self.lang.translate("Report of media analysis"))		

            headerText = headerText.replace('*case_number*', self.Report_Number_TF.getText())

            
            headerText = headerText.replace('*examiner*', self.Examiners_TF.getText())
            headerText = headerText.replace('*report_date*', datetime.datetime.today().strftime('%Y-%m-%d %H:%M'))
            headerText = headerText.replace('*lb_autopsy_ver*', self.lang.translate("Autopsy version"))	
            headerText = headerText.replace('*autopsy_ver*', self.lang.translate(autopsy_version))			
            headerText = headerText.replace('*description*',  self.Description_TF.getText())	
            headerText = headerText.replace('*from*', str(fileIndexStart))
            headerText = headerText.replace('*to*',  str(fileIndexEnd))
			
            
            headerText = headerText.replace('*current_page*', str(current_page))
            headerText = headerText.replace('*total_pages*', str(total_pages))
            nextBookmarkFileName = page_file_name + str(current_page + 1) + ".html"
            prevBookmarkFileName = page_file_name + str(current_page - 1) + ".html"
            
            if  current_page == 1:
                    prevBookmarkFileName = ''
            if  current_page == total_pages:
                    nextBookmarkFileName = ''
					
            headerText = headerText.replace('*bookmark_prev_file*', prevBookmarkFileName)
            headerText = headerText.replace('*bookmark_next_file*', nextBookmarkFileName)
                
                    
            headerText = headerText.replace('*date*', datetime.datetime.today().strftime('%d/%m/%Y'))
            headerText = headerText.replace('*encoding*', self.charEncoding)
            headerText = headerText.replace('*tag_name*',  self.lang.translate(tag_name))
            headerText = headerText.replace('*file_count*', str(number_of_tags))
 
			#labels
            headerText = headerText.replace('*lb_title*', self.lang.translate("Title"))	
            headerText = headerText.replace('*lb_case_number*',  self.lang.translate("Case Number"))	
            headerText = headerText.replace('*lb_examiner*', self.lang.translate("Examiner(s)"))	
            headerText = headerText.replace('*lb_report_date*', self.lang.translate("Report date"))
            headerText = headerText.replace('*lb_description*', self.lang.translate("Description"))	
            headerText = headerText.replace('*lb_tag*', self.lang.translate("Tag"))
            headerText = headerText.replace('*lb_file_count*', self.lang.translate("Number of files"))
            headerText = headerText.replace('*lb_files*', self.lang.translate("Files"))
            headerText = headerText.replace('*lb_description*', self.lang.translate("Description"))
            headerText = headerText.replace('*lb_print*', self.lang.translate("Print") )			
            headerText = headerText.replace('*lb_previous_page*', self.lang.translate("Previous page") )			
            headerText = headerText.replace('*lb_next_page*', self.lang.translate("next page") )						
            
			#dodaanie przycisków stron	
            buttons = self.create_page_buttons(page_file_name, current_page,total_pages)           				
            headerText = headerText.replace('*buttons*', buttons)
			
            page_file.write(headerText)
			
        except BaseException as e:		
            self.log(Level.INFO, str(e))
        
    def create_index_file(self, report_dir):
        index_file_name = os.path.join(report_dir, self.report_file_name)
        index_file = open(index_file_name, 'w')
        index_file.write('<?xml version="1.0" encoding="' + self.charEncoding + '"?>')
        index_file.write('<html xmlns="http://www.w3.org/1999/xhtml">')
        index_file.write(" ")
        index_file.write("<head>")
        index_file.write('    <meta http-equiv="Content-Type" content="text/html; charset='+ self.charEncoding+'"/>')
        index_file.write("    <title> " + Case.getCurrentCase().getNumber() + "</title>") 
        index_file.write("</head>")
        index_file.write(" ")
        index_file.write('<frameset cols="290,10%">')
        index_file.write('    <frame src="'+self.lang.translate("Report")+'/res/Menu.html" name="navigate" frameborder="0"/>')
        index_file.write('    <frame src="'+self.lang.translate("Report")+'/res/Info.html" name="contents" frameborder="1"/>')
        index_file.write("    <noframes/>")
        index_file.write("</frameset>")
        index_file.write(" ")
        index_file.write("</html>")
        index_file.close()
        
    def create_info_page(self, report_dir):
        # get case specific information to put in the information.html file
	
        try:  
            
            skCase = Case.getCurrentCase()	
			# otwiera plik  z szablonem strony info.html
            infoPath = os.path.join(self.module_dir,"html", "info.html").encode(self.charEncoding)
            
            infoFile = open(infoPath, 'r')           
            infoText = infoFile.read()
            autopsy_version=Version.getVersion()
            
            infoText = infoText.replace('*case_info*', self.lang.translate("Case Information"))
            infoText = infoText.replace('*title*', self.lang.translate("Report of media analysis"))		
            infoText = infoText.replace('*case_number*', self.Report_Number_TF.getText())
            infoText = infoText.replace('*examiner*', self.Examiners_TF.getText())
            infoText = infoText.replace('*report_date*', datetime.datetime.today().strftime('%Y-%m-%d %H:%M'))	
            infoText = infoText.replace('*description*',  self.Description_TF.getText())	
            infoText = infoText.replace('*encoding*',  self.charEncoding)
			
			#labels
            infoText = infoText.replace('*lb_title*', self.lang.translate("Title"))	
            infoText = infoText.replace('*lb_case_number*',  self.lang.translate("Case Number"))	
            infoText = infoText.replace('*lb_examiner*', self.lang.translate("Examiner(s)"))	
            infoText = infoText.replace('*lb_report_date*', self.lang.translate("Report date"))
            infoText = infoText.replace('*lb_description*', self.lang.translate("Description"))
            infoText = infoText.replace('*lb_attention*', self.lang.translate("ATTENTION"))	
            infoText = infoText.replace('*attention_info*', self.lang.translate("To view this report preferred browser is latest Google Chrome, Microsoft Edge or Firefox"))
            infoText = infoText.replace('*lb_autopsy_ver*', self.lang.translate("Autopsy version"))	
            infoText = infoText.replace('*autopsy_ver*', self.lang.translate(autopsy_version))
            
            #dodawanie informacji o żródlach danych
            infoText = infoText.replace('*lb_image_information*', self.lang.translate("Image information"))
			
            data_source_rows="<tr><th class=\"tdh\">"+self.lang.translate("Source name")+"</th><th class=\"tdh\">"+self.lang.translate("Tag name")+"</th><th class=\"tdright\" >"+self.lang.translate("Tagged files count")+"</th></tr>"
            for source in self.data_source_selected:
                data_source_rows+="<tr> <td class=\"tds\">"+str(source.Name)+"</td>  <td class=\"tds\"></td> <td class=\"tds\"> </td> </tr>"
                for tag in self.tags_selected:
                    data_source_rows+="<tr> <td></td><td class=\"tdr\">"+self.lang.translate(tag)+"</td><td class=\"tdright\">"+self.count_tags(tag,source.Id)+"</td>"
                                       
            infoText = infoText.replace('*source_name_row*', data_source_rows)
			
            # Open and write information.html file
            info_file_name = os.path.join(report_dir, "Info.html")
            info_file = open(info_file_name, 'w')
            info_file.write(infoText.encode(self.charEncoding))
	           
            
            # Close Info File        
            info_file.close()
            self.log(Level.INFO, "Info page created")
			
        except BaseException as e:		
            self.log(Level.INFO, str(e))
			
    def create_help_page(self, report_dir):
        
	
        try:  
            
            
			# otwiera plik  z szablonem strony Help.html
            helpPath = os.path.join(self.module_dir,"html", "Help.html").encode(self.charEncoding)
            
            helpFile = open(helpPath, 'r')           
            helpText = helpFile.read()
            
            helpText = helpText.replace('*encoding*', self.charEncoding)			
            helpText = helpText.replace('*lb_help_header*', self.lang.translate("Help"))
            helpText = helpText.replace('*lb_menu_items_header*', self.lang.translate("Menu's items:"))		   
            helpText = helpText.replace('*lb_summary_header*', self.lang.translate("Summary of analysis"))	
            helpText = helpText.replace('*summary_info*',  self.lang.translate("Case information: start page with informations about the case, like case number, forensic examiner, etc."))	
            helpText = helpText.replace('*help_info*', self.lang.translate("Help: this help page."))	
            helpText = helpText.replace('*lb_selected_evidences*', self.lang.translate("Selected Evidences"))
            helpText = helpText.replace('*selected_evidences_info*', self.lang.translate("Images (for example): page(s) containing name, link and others metadata of selected files for each evidence category (tag)."))
            helpText = helpText.replace('*lb_storage*', self.lang.translate("Storage and visualization of files"))	
            helpText = helpText.replace('*storage1*', self.lang.translate("Not all of the evidence files exported to this optical media can be opened up in the browser application. In this case, it can be needed the instalation of the proper application"))
            helpText = helpText.replace('*storage2*', self.lang.translate("All of the evidence files were exported to report folder *report_dir*/*tagged_files*."))
            helpText = helpText.replace('*tagged_files*', self.lang.translate("Tagged_Files"))	
            helpText = helpText.replace('*report_dir*', self.lang.translate("Report"))				
            helpText = helpText.replace('*storage3*', self.lang.translate(""))			
			
            	
            # Open and write information.html file
            help_file_name = os.path.join(report_dir, "Help.html")
            help_file = open(help_file_name, 'w')
            help_file.write(helpText.encode(self.charEncoding))
	           
            
            # Close help File        
            help_file.close()
	       
        except BaseException as e:		
            self.log(Level.INFO, str(e))			
        
    def create_menu_file(self, report_dir): 

        	
        # get case specific information to put in the information.html file
        skCase = Case.getCurrentCase()
 
        # Open and write information.html file
        menu_file_name = os.path.join(report_dir, "menu.html")
        menu_file = open(menu_file_name, 'w')
        
        menu_file.write('<?xml version="1.0" encoding="' + self.charEncoding + '"?>')
        menu_file.write('<html xmlns="http://www.w3.org/1999/xhtml">')
        menu_file.write(' ')
        menu_file.write('<head>')
        menu_file.write('    <meta http-equiv="Content-Type" content="text/html; charset='+ self.charEncoding+'"/>')
        menu_file.write('    <link rel="stylesheet" type="text/css" href="navigation.css"/>')
        menu_file.write('    <link rel="stylesheet" type="text/css" href="common.css"/>')
        menu_file.write('    <title>' + self.lang.translate("Summary") + '</title>')
        menu_file.write('</head>')
        menu_file.write(' ')
        menu_file.write('<body background="Background.gif">')
        menu_file.write(' ')
        menu_file.write('<!--    <img style="margin: 0px 70px" border="0" src="brasao.gif"/>-->')
        menu_file.write('    <img style="margin: 0px 10px" border="0" src="icon.ico"/>')
        menu_file.write('    <p> </p>')
        menu_file.write('    <div>')
        menu_file.write('        <h3><font color="white">' + self.lang.translate("Summary of analysis") + '<h3>')
        menu_file.write('        <a class="sectionLinks" target="contents" href="Info.html">')
        menu_file.write('            <span style="margin-left:5px"> ' + self.lang.translate("Case Information") + ' </span>')
        menu_file.write('        </a>')
        menu_file.write('        <div> </div>')
        menu_file.write('        <a class="sectionLinks" target="contents" href="Help.html">')
        menu_file.write('            <span style="margin-left:5px">' + self.lang.translate("Help")  + '</span>')
        menu_file.write('        </a>')
        menu_file.write('        <div> </div> ')
        menu_file.write('        <h3>' + self.lang.translate("Selected Evidences") + '<h3>')
        tag_number = 1
        for tag in self.tags_selected:
            menu_file.write('        <a class="sectionLinks" target="contents" href="' + self.lang.translate("Bookmark") + str(tag_number) + self.lang.translate("Page") + '1.html">')
            menu_file.write('            <span style="margin-left:0px">' + self.lang.translate(tag) + '</span>')
            menu_file.write('        </a>')
            tag_number = tag_number + 1
        menu_file.write(' ')
        menu_file.write('    </div>')
        menu_file.write(' ')
        menu_file.write('</body>')
        menu_file.write('</html>')
        menu_file.close()
        self.log(Level.INFO, "Menu file created")

    def onchange_lb(self, event):
        self.tags_selected[:] = []
        self.tags_selected = self.List_Box_LB.getSelectedValuesList()

    def onchange_sb(self, event):
        self.data_source_selected=[]
        selectedIx = self.List_Box_Sources.getSelectedIndices()	
        for i in selectedIx:
            self.data_source_selected.append(self.List_Box_Sources.getModel().getElementAt(i))
		
		
	# return string	with data source ids ex. "12,4589,45555"	
    def get_string_source_id_selected(self):
        ids=[]
        separtor=","
        for source in self.data_source_selected:
           ids.append(str(source.Id))
        return 	separtor.join(ids)		

    def find_tags(self):
        tag_list = []
        sql_statement = "SELECT distinct(display_name) u_tag_name FROM content_tags INNER JOIN tag_names ON content_tags.tag_name_id = tag_names.tag_name_id  INNER JOIN tsk_files on content_tags.obj_id = tsk_files.obj_id" +\
		                " where tsk_files.data_source_obj_id in ("+self.get_string_source_id_selected()+")"
        #self.log(Level.INFO, sql_statement)
        skCase = Case.getCurrentCase().getSleuthkitCase()
        dbquery = skCase.executeQuery(sql_statement)
        resultSet = dbquery.getResultSet()
        while resultSet.next():
             tag_list.append(resultSet.getString("u_tag_name"))
        dbquery.close()    
        return tag_list 
        
    def count_tags(self,tag_name,data_source_id):
        #tag_count = [];
        sql_statement = "SELECT count(*) count FROM content_tags INNER JOIN tag_names ON content_tags.tag_name_id = tag_names.tag_name_id  INNER JOIN tsk_files on content_tags.obj_id = tsk_files.obj_id" +\
		                " where tsk_files.data_source_obj_id in ("+str(data_source_id)+") and display_name='"+tag_name+"'"
        #self.log(Level.INFO, sql_statement)
        skCase = Case.getCurrentCase().getSleuthkitCase()
        dbquery = skCase.executeQuery(sql_statement)
        resultSet = dbquery.getResultSet() 
        tag_count= resultSet.getString("count")       
        dbquery.close()    
        return tag_count         
        
		
    #sortuje wytypowane pliki wg kryterium
    def sort_tags(self, tags_to_sort,sort_criterion):
        self.log(Level.INFO, "Sorting started")
        self.tags_to_sort=tags_to_sort
        self.sort_criterion=sort_criterion		
        self.quicksort(0, len(self.tags_to_sort)-1)
        sorted=self.tags_to_sort
        self.log(Level.INFO, "Sorting finished")
        return     sorted	

    #quick sort
    def quicksort(self,left, right):
        i=1
        i=int((left+right)/2)
        pivot=self.tags_to_sort[i]
        self.tags_to_sort[i]=self.tags_to_sort[right]
        j=left
        i=left		
        for i in range(left,right):
            item=self.get_item_to_sort(self.tags_to_sort[i],self.sort_criterion)
            pivot_item=self.get_item_to_sort(pivot,self.sort_criterion)
            if (item < pivot_item):
               	swap=self.tags_to_sort[i]
                self.tags_to_sort[i]=self.tags_to_sort[j]
                self.tags_to_sort[j]=swap
                j+=1
        self.tags_to_sort[right]=self.tags_to_sort[j]
        self.tags_to_sort[j]=pivot
        if (left<j-1):   
		    self.quicksort(left, j-1)
        if (j+1<right):   
		    self.quicksort(j+1, right) 			
		
    #zwraca element wg, którego zachodzi sortowanie
    def get_item_to_sort(self, tagContent,sort_criterion ):


        if sort_criterion=='Date Modified':
            return tagContent.getContent().getMtimeAsDate()
        if sort_criterion=='Date Created':
            return tagContent.getContent().getCtimeAsDate()
        if sort_criterion=='Date Accessed':
            return tagContent.getContent().getAtimeAsDate()			
        if sort_criterion=='File Path':
            return tagContent.getContent().getUniquePath()	
        if sort_criterion=='File Name':
            return tagContent.getContent().getName()	
        if sort_criterion=='MD5 Hash':
            return (tagContent.getContent().getMd5Hash())	
        if sort_criterion=='SHA256 Hash':
            return (tagContent.getContent().getSha256Hash())	
        if sort_criterion=='MIME Type':
            return tagContent.getContent().getMIMEType()
        if sort_criterion=='File Size':
            return tagContent.getContent().getSize()				
                   
        		
		
	#tworzy foldery wg nazw tagów	
    def create_taged_files_folder(self,report_files_dir, tagName):
	
        tag_files_dir = os.path.join(report_files_dir,tagName)        
        try:
            os.mkdir(tag_files_dir)
        except BaseException as e:		
            self.log(Level.INFO, str(e))
	
    def create_page_buttons(self,page_file_name,current_page,total_pages):
		#dodaanie przycisków stron	
        buttons=""
        button='<input type="button" *style*' + 'onclick="location.href='+ "'" + page_file_name + '*page_number*.html' + "'" + ';"' + 'value="*page_number*" />\n	'
        if total_pages > 1:
            for x in range(1, total_pages+1):
                style =""						
                if (x==	current_page):
                    style='style="background-color:black;color:white;"'				
                buttons+= button.replace("*page_number*",str(x))
                buttons = buttons.replace("*style*",style)
        return buttons				
     
    def standardize_folder_name(self, folder_name):
        sign_to_remove =["#","%","&","*",":","?","/","\\","|"]
        for x in sign_to_remove:
            folder_name = folder_name.replace(x,'_')
        return folder_name
		
    def get_extension(self,filename):
        basename = os.path.basename(filename)  # os independent
        ext = '.'.join(basename.split('.')[1:])
        return ext if ext else None

    def find_result(self,obj_id,artifact_type_id,blackboard_attribute_type_name):
        result_array = []
        try:		
            sql_statement = "select blackboard_attribute_types.display_name," +\
		     				"case blackboard_attributes.value_type " +\
		     				"when 3 then cast(round(blackboard_attributes.value_double,5) as varchar(50)) " +\
		     				"when 5 then cast(blackboard_attributes.value_int64 as varchar(50)) " +\
		     				"when 0 then cast(blackboard_attributes.value_text as varchar(50)) " +\
		     				"end " +\
		     				"value " +\
		     				"from blackboard_artifacts " +\
		     				"left join blackboard_attributes USING (ARTIFACT_ID) " +\
		     				"left join blackboard_attribute_types on (blackboard_attributes.attribute_type_id = blackboard_attribute_types.attribute_type_id) " +\
		     				"where blackboard_artifacts.obj_id='"+str(obj_id)+"' AND blackboard_artifacts.artifact_type_id='"+str(artifact_type_id)+"';"
            #self.log(Level.INFO,sql_statement)							
            skCase = Case.getCurrentCase().getSleuthkitCase()
            dbquery = skCase.executeQuery(sql_statement)
            resultSet = dbquery.getResultSet()			
            while resultSet.next():
                result_array.append([resultSet.getString("display_name"),resultSet.getString("value")])
            dbquery.close()			
        except BaseException as e:		
            self.log(Level.INFO,'Błąd'+ str(e))
		
        return result_array
        
        #pobiera listę data source 
    def get_data_sources(self):
        source_list = []
        skCase = Case.getCurrentCase().getSleuthkitCase()
        resultSet = skCase.getDataSources()
        for  source in resultSet:
             source_list.append(Data_Source(source.getId(),source.getName()))   
        return source_list		

    def eventListener(self,event):
        item = event.item 
        self.log(Level.INFO, str(item))			
        self.lang.setLanguageTo(item)
        self.Label_0.setText(self.lang.translate("Number of Object to Display per page"))
        self.Label_1.setText(self.lang.translate("Report language"))
        self.Label_2.setText(self.lang.translate("Report Number To Appear on Case Info"))
        self.Label_3.setText(self.lang.translate("Examiner(s) To Appear on Case Info"))
        self.Label_4.setText(self.lang.translate("Description To Appear on Case Info"))
        self.Label_5.setText(self.lang.translate( "Tags to Select for Report:")) 
        self.Blank_5.setText(self.lang.translate( "Sort files by:"))

# if file extention is invalid returns valid file extention, if file extention is valid returns empty string
    def get_valid_file_ext(self, file_name, MimeType):
        ext=self.get_extension(file_name)
        mime_ext=MimeType.split('/')[1]	
        extDict={
            'video/quicktime':'mov',
            'video/x-m4v':'m4v',
            'audio/vnd.wave':'wave',
            'audio/vorbis':'ogg',
            'audio/x-flac':'flac',
            'image/vnd.microsoft.icon':'ico',
            'image/x-portable-floatmap':'pbm',
            'image/jpeg':'jpg'			
            }
        if (ext==mime_ext):
            return ""
        if (MimeType in extDict):
            if (ext==extDict[MimeType]):
                return ""
            else:
                return extDict[MimeType]
        else:
            return mime_ext

class Data_Source():
    
    def __init__(self, Id, Name):   	 
        self.Id = Id
        self.Name = Name
    def __str__(self):
	    return self.Name		
    def __repr__(self):    	
        return self.Name

		
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