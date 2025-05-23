__author__ = 'Lokesh'

tableDictionary={
    'partner':'programs_partner',
    'country':'geographies_country',
    'state':'geographies_state',
    'district':'geographies_district',
    'block':'geographies_block',
    'village':'geographies_village',
    'animator':'people_animatorwisedata',
    'person':'people_person',
    'persongroup':'people_persongroup',
    'video':'videos_video',
    'language':'videos_language',
    'category':'videos_category',
    'subcategory':'videos_subcategory',
    'videovideop':'videos_video_videopractice',
    'videopractice':'videos_videopractice',
    'tag':'videos_tag',
    'videotag':'videos_video_tags',
    'videovideop':'videos_video_videopractice',
    'sector':'videos_practicesector',
    'practice':'videos_practice',
    'topic':'videos_practicetopic',
    'numScreening':'activities_screeningwisedata',
    'numAdoption':'activities_personadoptpractice',
    'attendance':'activities_personmeetingattendance',
    'numPerson':'people_person',
    'numAnimator':'people_animatorwisedata',
    'numVillageAdoption':'geographies_village',
    'numVillageScreening': 'activities_screeningwisedata',
    'numBlockScreening':'geographies_block',
    'numBlock':'geographies_block',
    'numBlockAdoption':'geographies_block',
    'numVillage':'geographies_village',
    'listPerson':'people_person',
    'listAnimator':'people_animatorwisedata',
    'listVideoScreened':'activities_screeningwisedata',
    'numVideoScreened':'activities_screeningwisedata',
    'listVideoProduced':'videos_video',
    'numVideoProduced':'videos_video',
    'list':'self',
    'listGroup':'people_persongroup',
    'listVillage':'geographies_village',
    'listBlock':'geographies_block',
    'listDistrict':'geographies_district',
    'listState':'geographies_state',
    'listCountry':'geographies_country',
    'listPartner':'programs_partner'
}

whereDictionary={
    'partner':'id',
    'country':'id',
    'state':'id',
    'district':'id',
    'block':'id',
    'village':'id',
    'animator':'animator_id',
    'person':'id',
    'persongroup':'id',
    'video':'id',
    'language':'id',
    'category':'id',
    'subcategory':'id',
    'videopractice':'id',
    'tag':'id',
    'videotag':'tag_id',
    'videovideop':'videopractice_id',
    'sector':'id',
    'practice':'id',
    'topic':'id',
    'numScreening':'screening_date',
    'numAdoption':'date_of_adoption',
    'attendance':'activities_screeningwisedata.screening_date',
    'numPeople':'time_created',
    'numAnimator':'time_created',
    'listPerson':'time_created',
    'listAnimator':'time_created',
    'listVideoScreened':'activities_screeningwisedata.screening_date',
    'numVillageAdoption':'activities_personadoptpractice.date_of_adoption',   
    'numVillageScreening':'activities_screeningwisedata.screening_date',
    'numBlockScreening':'activities_screeningwisedata.screening_date',
    'numBlockAdoption':'activities_personadoptpractice.date_of_adoption', 
    'numVideoScreened':'activities_screeningwisedata.screening_date',
    'listVideoProduced':'production_date',
    'numVideoProduced':'production_date',
    'list':'self',
    'listGroup':'time_created',
    'listVillage':'time_created',
    'listBlock':'time_created',
    'listDistrict':'time_created',
    'listState':'time_created',
    'listCountry':'time_created',
    'listPartner':'time_created',
    'numVillage':'time_created',
    'numBlock' : 'time_created'
}


categoryDictionary={
    'geographies':['country','state','district','block','village'],
    'partitionCumValues':{'listAnimator':'animator','listVideoScreened':'video','listVideoProduced':'video','listPerson':'person',
                          'listGroup':'persongroup', 'listVillage':'village','listBlock':'block','listDistrict':'district','listState':'state',
                          'listCountry':'country','listPartner':'partner','numScreening':'numScreening','numVillageScreening':'video',
                          'numVillageAdoption':'numVillage','numBlockScreening':'numBlock','numBlockAdoption':'numBlock','numVillage':'numVillage','numBlock':'numBlock'}
}

groupbyDictionary={
    'partner':'id',
    'country':'id',
    'state':'id',
    'district':'id',
    'block':'id',
    'village':'id',
    'animator':'animator_id',
    'person':'id',
    'persongroup':'id',
    'video':'id',
    'language':'id',
    'category':'id',
    'subcategory':'id',
    'tag':'id',
    'videotag':'tag_id',
    'videovideop':'videopractice_id',
    'videopractice':'id',
    'sector':'id',
    'practice':'id',
    'topic':'id',
    'numBlockAdoption':False,
    'numVillageAdoption':False,
    'numScreening':False,
    'numAdoption':False,
    'attendance':False,
    'numPerson':False,
    'numAnimator':False,
    'numBlockScreening':False,
    'numVillageScreening':False,
    'numBlock':False,   
    'numVillage':False, 
    'listPerson':'id',
    'listAnimator':'animator_id',
    'numVideoScreened':False,
    'numVideoProduced':False,
    'list':'self',
    'listVideoProduced':'id',
    'listVideoScreened':'video_id',
    'listGroup':'id',
    'listVillage':'id',
    'listBlock':'id',
    'listDistrict':'id',
    'listState':'id',
    'listCountry':'id',
    'listPartner':'id'
}

selectDictionary={
    'partner':{'id':False,'partner_name':True},
    'country':{'id':False,'country_name':True},
    'state':{'id':False,'state_name':True},
    'district':{'id':False,'district_name':True},
    'block':{'id':False,'block_name':True},
    'village':{'id':False,'village_name':True},
    'animator':{'animator_id':False,'animator_name':True,'gender':False},
    'person':{'id':False,'person_name':True,'gender':False},
    'persongroup':{'id':False,'group_name':True},
    'video':{'id':False,'title':True,'youtubeid':True},
    'category':{'id': False,'category_name':True},
    'subcategory':{'id': False,'subcategory_name':True},
    'videopractice':{'id':False,'videopractice_name':True},
    'tag':{'id':False,'tag_name':True},
    'video_tag':{'id':False},
    'language':{'id':False,'language_name':True},
    'sector':{'id':False,'name':True},
    'practice':{'id':False,'practice_name':True},
    'topic':{'id':False,'name':True},
    'numScreening':{'count(screening_id)':False,'count(distinct screening_id)':True,'video_youtubeid':False},
    'numAdoption':{'count(distinct person_id)':True,'count(person_id)':True},
    'attendance':{'count(person_id)':False,'count(distinct person_id)':True},
#    'numPeople':{'count(id)':True,'count(distinct id)':False},
    'numBlockAdoption':{'count(id)':False,'count(distinct id)':True},
    'numBlockScreening':{'count(id)':False,'count(distinct id)':True},
    'numVillageAdoption':{'count(id)':False,'count(distinct id)':True},
    'numVillageScreening':{'count(village_id)':False,'count(distinct village_id)':True,'distinct(video_title)':True,'video_id':True,'video_youtubeid':True},
    'numVillage':{'count(id)':False,'count(distinct id)':True},
    'numBlock':{'count(id)':False,'count(distinct id)':True},
    'numAnimator':{'count(animator_id)':True,'count(distinct animator_id)':False},
    'listPerson':{'distinct(person_name)':True,'gender':False},
    'listAnimator':{'distinct(animator_name)':True,'gender':False},
    'numVideoScreened':{'count(video_id)':False,'count(distinct video_id)':True},
    'numVideoProduced':{'count(id)':True,'count(distinct id)':False},
    'list':'self',
    'listVideoProduced':{'id':True,'youtubeid':True,'distinct(title)':True},
    'listVideoScreened':{'video_id':True,'distinct(video_title)':True,'video_youtubeid':True},
    'listGroup':{'id':False,'distinct(group_name)':True},
    'listVillage':{'distinct(village_name)':True},
    'listBlock':{'distinct(block_name)':True},
    'listDistrict':{'distinct(district_name)':True},
    'listState':{'distinct(state_name)':True},
    'listCountry':{'distinct(country_name)':True},
    'listPartner':{'distinct(partner_name)':True}

}

headerDictionary = {
    'partner':{'id':'Partner ID','partner_name':'Partner Name'},
    'country':{'id':'Country ID','country_name':'Country Name'},
    'state':{'id':'State ID','state_name':'State Name'},
    'district':{'id':'District ID','district_name':'District Name'},
    'block':{'id':'Block ID','block_name':'Block Name'},
    'village':{'id':'Village ID','village_name':'Village Name'},
    'animator':{'animator_id':'Animator ID','animator_name':'Animator Name','gender':'Animator Gender'},
    'person':{'id':'Person ID','person_name':'Person Name','gender':'Person Gender'},
    'persongroup':{'id':'Person Group ID','group_name':'Group Name'},
    'video':{'id':'Video ID','title':'Video Title','youtubeid':'Youtube ID','category_id':'Video Category','subcategory_id':'Video Subcategory'},
    'language':{'id':'Video Language ID','language_name':'Video Language'},
    'category':{'id':'Video Category ID','category_name':'Video Category'},
    'subcategory':{'id':'Video SubCategory ID','subcategory_name':'Video SubCategory'},
    'videopractice':{'id':'Video VideoPractice ID','videopractice_name':'Video VideoPractice' },
    'tag':{'id':'Video Tag ID','tag_name':'Video Tag'},
    'sector':{'id':'Sector ID','name':'Sector Name'},
    'practice':{'id':'Practice ID','practice_name':'Practice Name'},
    'topic':{'id':'Topic ID','name':'Topic'},
    'numScreening':{'count(screening_id)':'Number of Screening','count(distinct screening_id)':'Number of Screenings','video_youtubeid':'Youtube ID'},
    'numAdoption':{'count(person_id)':'Number of Adoptions','count(distinct person_id)':'Distinct Adopters'},
    'attendance':{'count(person_id)':'Number of Viewers','count(distinct person_id)':'Unqiue Number of Viewers'},
#    'numPeople':{'count(id)':True,'count(distinct id)':False},
    'numBlockAdoption':{'count(id)':'Number of Blocks','count(distinct id)':'Number of Blocks'},
    'numBlockScreening':{'count(id)':'Number of Blocks','count(distinct id)':' Number of Blocks'},
    'numVillageAdoption':{'count(id)':'Number of Villages','count(distinct id)':' Number of Villages'},
    'numVillageScreening':{'count(village_id)':'Number of Villages','count(distinct village_id)':' Number of Villages','distinct(video_title)':'Video Screened','video_id':'Video ID','video_youtubeid':'Youtube ID'},
    'numVillage':{'count(id)':'Number of Villages','count(distinct id)':'Number of Villages'},
    'numBlock':{'count(id)':'Number of Blocks','count(distinct id)':'Number of Blocks'},
    'numAnimator':{'count(animator_id)':'Number of Animator','count(distinct animator_id)':'Number of '},
    'listPerson':{'distinct(person_name)':'Person Name','gender':'Person Gender'},
    'listAnimator':{'distinct(animator_name)':'Animator Name','gender':'Animator Gender'},
    'numVideoScreened':{'count(video_id)':'Number of Videos Screened','count(distinct video_id)':'Number of Unique Videos Screened'},
    'numVideoProduced':{'count(id)':'Number of Videos Produced','count(distinct id)':'Number of Unique Videos Produced'},
    'list':'self',
    'listVideoProduced':{'id':'Video ID','youtubeid':'Youtube ID','distinct(title)':'Video Produced'},
    'listVideoScreened':{'video_id':'Video ID','distinct(video_title)':'Video Screened','video_youtubeid':'Youtube ID'},
    'listGroup':{'id':'Group ID','distinct(group_name)':'Group Name'},
    'listVillage':{'distinct(village_name)':'Village Name'},
    'listBlock':{'distinct(block_name)':'Block Name'},
    'listDistrict':{'distinct(district_name)':'District Name'},
    'listState':{'distinct(state_name)':'State Name'},
    'listCountry':{'distinct(country_name)':'Country Name'},
    'listPartner':{'distinct(partner_name)':'Partner Name'}
}

orderDictionary = {
    'partner':0,
    'country':1,
    'state':2,
    'district':3,
    'block':4,
    'village':5,
    'animator':6,
    'video':7,
    'persongroup':10,
    'person':11,
    'category':8,
    'subcategory':9,
    'videopractice':12,
    'tag':13,

}


checkValueSpecial =[
    'list',
    'numVillage',
    'numBlock'
]

