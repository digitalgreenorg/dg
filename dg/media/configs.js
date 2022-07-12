define([], function () {
  // //This template would be passed the json of inline model and shall produce the desired row
  //     TODO: maybe instead of relying on users to use templating lang we should fill the rows ourselves in js code, like we are doing in form!

  var village_configs = {
    page_header: "Village",
    config_English: "Villages",
    config_हिन्दी: "गाँव",
    config_Français: "Villages",
    list_elements_English: [
      { header: "ID", element: "online_id" },
      { header: "Name", element: "village_name" },
      { element: "block_name" },
      { element: "start_date" },
      { header: "State", element: "state_name" },
    ],
    list_elements_हिन्दी: [
      { header: "आईडी", element: "online_id" },
      { header: "नाम", element: "village_name" },
      { header: "ब्लॉक का नाम", element: "block_name" },
      { header: "आरंभ होने की तिथि", element: "start_date" },
      { header: "राज्य का नाम", element: "state_name" },
    ],
    list_elements_Français: [
      { header: "Identité", element: "online_id" },
      { header: "Nom", element: "village_name" },
      { header: "Nom unite geographique", element: "block_name" },
      { header: "Date de début", element: "start_date" },
      { header: "Etat", element: "state_name" },
    ],
    rest_api_url: "/coco/api/v2/village/",
    entity_name: "village",
    dashboard_display: {
      listing: true,
      add: false,
    },
    sort_field: "village_name",
  };

  var mediator_configs = {
    page_header: "Mediator",
    config_English: "Mediators",
    config_हिन्दी: "मध्यस्थ",
    config_Français: "Disséminateurs",
    labels_हिन्दी: {
      mediator: "मध्यस्थ",
      name: "नाम",
      district: "जिला",
      gender: "लिंग",
      phone_number: "फ़ोन नंबर",
      assigned_villages: "नियुक्त किए गये गाँव",
    },
    labels_Français: {
      mediator: "Disséminateurs",
      name: "Nom",
      district: "Commune",
      gender: "Genre",
      phone_number: "Numéro de téléphone",
      assigned_villages: "Villages assignés",
    },
    labels_English: {
      mediator: "Mediator",
      name: "Name",
      district: "District",
      gender: "Gender",
      phone_number: "Phone Number",
      assigned_villages: "Assigned Villages",
    },
    list_elements_हिन्दी: [
      { header: "आईडी", element: "online_id" },
      { header: "नाम", element: "name" },
      {
        header: "नियुक्त किए गये गाँव",
        subelement: "village_name",
        element: "assigned_villages",
      },
    ],
    list_elements_Français: [
      { header: "Identité", element: "online_id" },
      { header: "Nom", element: "name" },
      {
        header: "Villages assignés",
        subelement: "village_name",
        element: "assigned_villages",
      },
    ],
    list_elements_English: [
      { header: "ID", element: "online_id" },
      { element: "name" },
      { subelement: "village_name", element: "assigned_villages" },
    ],
    add_template_name: "mediator_add_edit_template",
    edit_template_name: "mediator_add_edit_template",
    rest_api_url: "/coco/api/v2/mediator/",
    entity_name: "mediator",
    unique_together_fields: ["name", "gender", "district.id"],
    sort_field: "name",
    inc_table_name: "animator",
    foreign_entities: {
      village: {
        assigned_villages: {
          placeholder: "id_ass_villages",
          name_field: "village_name",
        }, //name of html element in form/ attribute name in json: {placeholder: "id of html element in form", name_field: "attribute in foreign entity's json "}
      },
      district: {
        district: {
          placeholder: "id_district",
          name_field: "district_name",
        },
      },
    },
    form_field_validation: {
      ignore: [],
      rules: {
        name: {
          required: true,
          minlength: 2,
          maxlength: 100,
          allowedChar: true,
        },
        gender: "required",
        phone_no: {
          digits: true,
          maxlength: 10,
        },
        assigned_villages: "required",
        district: "required",
      },
      messages: {
        name: {
          required: "Mediator name is required",
          minlength: "Mediator name should contain at least 2 characters",
          maxlength: "Mediator name should contain at most 100 characters",
          allowedChar:
            "Mediator name should contain only english and local language characters",
        },
        gender: "Gender is required",
        phone_no: {
          digits: "Phone number should contain only digits",
          maxlength: "Phone number should not contain more than 10 digits",
        },
        assigned_villages: "Assigned villages are required",
        district: "District is required",
      },

      highlight: function (element, errorClass, validClass) {
        $(element).parent("div").parent("div").addClass("error");
      },
      unhighlight: function (element, errorClass, validClass) {
        $(element).parent("div").parent("div").removeClass("error");
      },
      errorElement: "span",
      errorClass: "help-inline red-color",
      errorPlacement: function (label, element) {
        element.parent().append(label);
      },
    },
  };

  var video_configs = {
    page_header: "Video",
    config_English: "Videos",
    config_हिन्दी: "वीडियो",
    config_Français: "Vidéos",
    labels_हिन्दी: {
      video: "वीडियो",
      title: "शीर्षक",
      video_type: "वीडियो का प्रकार",
      production_date: "उत्पादन की तिथि",
      language: "भाषा",
      benefit: "लाभ",
      village: "गाँव",
      production_team: "वीडियो उत्पादन टीम",
      category: "श्रेणी",
      subcategory: "उप श्रेणी",
      videopractice: "विडियो में दिखाई गई क्रिया",
      tags: "टैग",
      youtubeid: "यूट्यूब आईडी",
      reviewed_by: "द्वारा अनुमोदित",
      reviewer: "संगठन",
      approval_date: "स्वीकृति तिथि",
      add_row: "खाली पंक्तियाँ जोड़े",
      sr_no: "क्रम संख्या",
      non_n: "अति आवश्यक बातें",
      physically_verifiable: "जाँच करने योग्य",
      direct_beneficiaries: "सीधा लाभार्थियों",
      self_reported_behaviour2: "Self Reported Behaviour2",
      self_reported_behaviour1: "Self Reported Behaviour1",
    },
    labels_Français: {
      video: "Vidéos",
      title: "Titre",
      video_type: "Type de vidéo",
      production_date: "Date de production",
      language: "Langue",
      benefit: "Bénéfice",
      village: "Villages",
      production_team: "Equipe de production",
      category: "Catégorie",
      subcategory: "Sous-catégorie",
      videopractice: "La pratique vidéo",
      tags: "Mots clés",
      youtubeid: "Identité Youtube",
      reviewed_by: "Approuvé par",
      reviewer: "organisation",
      approval_date: "Date de validation",
      add_row: "ajouter des lignes",
      sr_no: "Serie de Numéro",
      non_n: "Non négociables",
      physically_verifiable: "Physiquement vérifiable",
      direct_beneficiaries: "Bénéficiaires directs",
      self_reported_behaviour2: "Self Reported Behaviour2",
      self_reported_behaviour1: "Self Reported Behaviour1",
    },

    labels_English: {
      video: "Video",
      title: "Title",
      video_type: "Video Type",
      production_date: "Production Date",
      language: "Language",
      benefit: "Benefit",
      village: "Village",
      production_team: "Production Team",
      category: "Category",
      subcategory: "Sub Category",
      videopractice: "Video Practice",
      tags: "Tags",
      youtubeid: "YouTube ID",
      reviewed_by: "Approved By",
      reviewer: "Organization",
      approval_date: "Approval Date",
      add_row: "Add Empty Rows",
      sr_no: "Sr. No.",
      non_n: "Non Negotiables",
      physically_verifiable: "Physically Verifiable",
      direct_beneficiaries: "DirectBeneficiaries",
      srb: "Self Reported Behaviour",
      self_reported_behaviour2: "Self Reported Behaviour2",
      self_reported_behaviour1: "Self Reported Behaviour1",
    },
    list_elements_हिन्दी: [
      { header: "आईडी", element: "online_id" },
      { header: "शीर्षक", element: "title" },
      { header: "गाँव", element: "village.village_name" },
      { header: "उत्पादन की तिथि", element: "production_date" },
    ],
    list_elements_Français: [
      { header: "Identité", element: "online_id" },
      { header: "Titre", element: "title" },
      { header: "Villages", element: "village.village_name" },
      { header: "Date de production", element: "production_date" },
    ],
    list_elements_English: [
      { header: "ID", element: "online_id" },
      { element: "title" },
      { header: "Village", element: "village.village_name" },
      { header: "Production Date", element: "production_date" },
    ],
    add_template_name: "video_add_edit_template",
    edit_template_name: "video_add_edit_template",
    rest_api_url: "/coco/api/v2/video/",
    entity_name: "video",
    dependent_element_div_hide: "label_direct_beneficiaries",
    parent_element_to_hide: "direct_beneficiaries",
    parent_element_label_to_hide: "label_direct_beneficiaries",
    unique_together_fields: ["title", "production_date", "village.id"],
    sort_field: "title",
    foreign_entities: {
      mediator: {
        production_team: {
          placeholder: "id_production_team",
          name_field: "name",
        },
      },

      village: {
        village: {
          placeholder: "id_village",
          name_field: "village_name",
        },
      },
      language: {
        language: {
          placeholder: "id_language",
          name_field: "language_name",
        },
      },
      category: {
        category: {
          placeholder: "id_category",
          name_field: "category_name",
          parent_name_field: "parent_category",
        },
      },
      subcategory: {
        subcategory: {
          placeholder: "id_subcategory",
          name_field: "subcategory_name",
          dependency: [
            {
              source_form_element: "category",
              dep_attr: "category",
            },
          ],
        },
      },
      videopractice: {
        videopractice: {
          placeholder: "id_videopractice",
          name_field: "videopractice_name",
          dependency: [
            {
              source_form_element: "subcategory",
              dep_attr: "subcategory",
            },
          ],
        },
      },

      tag: {
        tags: {
          placeholder: "id_tags",
          name_field: "tag_name",
        },
      },

      directbeneficiaries: {
        direct_beneficiaries: {
          placeholder: "id_direct_beneficiaries",
          name_field: "direct_beneficiaries_category",
          dependency: [
            {
              source_form_element: "category",
              dep_attr: "category",
            },
          ],
        },
      },
    },
    inline: {
      entity: "nonnegotiable",
      validation_chk: "#non_negotiable0",
      default_num_rows: 5,
      add_row: 1,
      req_nonnegotiable: 0,
      error_message: "Add Non-negotiable",
      template: "nonnegotiable_inline",
      joining_attribute: {
        host_attribute: ["id", "title"],
        inline_attribute: "video",
      },
      header: "nonnegotiable_inline_header",
      borrow_attributes: [],
      foreign_entities: {
        video: {
          video: {
            placeholder: "id_video",
            name_field: "title",
          },
        },
      },
    },

    form_field_validation: {
      ignore: ".donotvalidate",
      rules: {
        title: {
          required: true,
          minlength: 2,
          maxlength: 200,
          // allowedChar: true
        },
        video_type: "required",
        production_date: {
          required: true,
          // validateDate: true
        },
        reviewer: "required",
        reviewed_by: "required",
        language: "required",
        benefit: {
          minlength: 2,
          maxlength: 500,
          // allowedChar: true
        },
        village: "required",
        production_team: "required",
        category: "required",
        subcategory: "required",
        videopractice: "required",
        approval_date: {
          dateOrder: { production_date: "production_date" },
          validateDate: true,
        },
        youtubeid: {
          maxlength: 20,
        },
      },
      messages: {
        title: {
          required: "Video title is required",
          minlength: "Video title should contain at least 2 characters",
          maxlength: "Video title should contain at most 200 characters",
          // allowedChar: 'Video title should only contain alphabets and local language characters'
        },
        video_type: "Video type is required",
        production_date: {
          required: "Video production date is required",
          validateDate: "Enter video production date in the form of YYYY-MM-DD",
        },
        language: "Language is required",
        benefit: {
          minlength: "Benefit should contain at least 2 characters",
          maxlength: "Benefit should contain at most 500 characters",
          // allowedChar: "summary should not contain special characters"
        },
        village: "Village is required",
        production_team: "Production team is required",
        category: "Category is required",
        subcategory: "Subcategory is required",
        videopractice: "Videopractice is required",
        approval_date: {
          validateDate: "Enter Approval Date in the form of YYYY-MM-DD",
          dateOrder: "Approval date should be later than production date",
        },
        youtubeid: {
          maxlength: "YoutubeID should contain at most 20 characters",
        },
      },

      highlight: function (element, errorClass, validClass) {
        $(element).parent("div").parent("div").addClass("error");
      },
      unhighlight: function (element, errorClass, validClass) {
        $(element).parent("div").parent("div").removeClass("error");
      },
      errorElement: "span",
      errorClass: "help-inline red-color",
      errorPlacement: function (label, element) {
        element.parent().append(label);
      },
    },
  };

  var language_configs = {
    config_English: "Languages",
    config_हिन्दी: "भाषा",
    config_Français: "Langue",
    rest_api_url: "/coco/api/v2/language/",
    entity_name: "language",
    sort_field: "language_name",
    dashboard_display: {
      listing: false,
      add: false,
    },
  };

  var tag_configs = {
    config_English: "Tags",
    config_हिन्दी: "भाषा",
    config_Français: "Tags",
    rest_api_url: "/coco/api/v2/tag/",
    entity_name: "tag",
    sort_field: "tag_name",
    dashboard_display: {
      listing: false,
      add: false,
    },
  };

  var category_configs = {
    config_English: "Categories",
    config_हिन्दी: "श्रेणी",
    config_Français: "Catégorie",
    rest_api_url: "/coco/api/v2/category/",
    entity_name: "category",
    sort_field: "category_name",
    dashboard_display: {
      listing: false,
      add: false,
    },
  };

  var frontlineworkerpresent_configs = {
    config_English: "FrontLineWorkerPresent",
    config_हिन्दी: "FrontLineWorkerPresent",
    config_Français: "FrontLineWorkerPresent",
    rest_api_url: "/coco/api/v2/frontlineworkerpresent/",
    entity_name: "frontlineworkerpresent",
    sort_field: "worker_type",
    dashboard_display: {
      listing: false,
      add: false,
    },
  };

  var parent_category_configs = {
    config_English: "ParentCategory",
    config_हिन्दी: "श्रेणी",
    config_Français: "Catégorie",
    rest_api_url: "/coco/api/v2/parentcategory/",
    entity_name: "parentcategory",
    sort_field: "parent_category_name",
    dashboard_display: {
      listing: false,
      add: false,
    },
  };

  var directbeneficiaries_configs = {
    config_English: "DirectBeneficiaries",
    config_हिन्दी: "सीधा लाभार्थियों",
    config_Français: "Bénéficiaires directs",
    rest_api_url: "/coco/api/v2/directbeneficiaries/",
    entity_name: "directbeneficiaries",
    sort_field: "direct_beneficiaries_category",
    dashboard_display: {
      listing: false,
      add: false,
    },
  };

  var subcategory_configs = {
    config_English: "Sub Categories",
    config_हिन्दी: "उप श्रेणी",
    config_Français: "Sous-catégorie",
    rest_api_url: "/coco/api/v2/subcategory/",
    entity_name: "subcategory",
    sort_field: "subcategory_name",
    foreign_entities: {
      category: {
        category: {
          placeholder: "id_category",
          name_field: "category_name",
        },
      },
    },
    dashboard_display: {
      listing: false,
      add: false,
    },
  };

  var videopractice_configs = {
    config_English: "Video Practices",
    config_हिन्दी: "विडियो में दिखाई गई क्रिया",
    config_Français: "La pratique vidéo",
    rest_api_url: "/coco/api/v2/videopractice/",
    entity_name: "videopractice",
    sort_field: "videopractice_name",
    foreign_entities: {
      subcategory: {
        subcategory: {
          placeholder: "id_subcategory",
          name_field: "subcategory_name",
        },
      },
    },
    dashboard_display: {
      listing: false,
      add: false,
    },
  };

  var nonnegotiable_configs = {
    config_English: "Non Negotiables",
    config_हिन्दी: "अति आवश्यक बातें",
    config_Français: "Non négociables",
    rest_api_url: "/coco/api/v2/nonnegotiable/",
    entity_name: "nonnegotiable",
    sort_field: "non_negotiable",
    foreign_entities: {
      video: {
        video: {
          placeholder: "id_video",
          name_field: "title",
        },
      },
    },
    dashboard_display: {
      listing: false,
      add: false,
    },
  };

  var district_configs = {
    config_English: "Districts",
    config_हिन्दी: "जिला",
    config_Français: "Commune",
    rest_api_url: "/coco/api/v2/district/",
    entity_name: "district",
    sort_field: "district_name",
    dashboard_display: {
      listing: false,
      add: false,
    },
  };

  var group_configs = {
    page_header: "Group",
    config_English: "Groups",
    config_हिन्दी: "ग्राम संगठन",
    config_Français: "Groupes",
    labels_हिन्दी: {
      group: "ग्राम संगठन",
      name: "नाम",
      village: "गाँव",
      person_name: "सदस्य का नाम",
      father_name: "पिता/पति का नाम",
      age: "आयु",
      gender: "लिंग",
      phone_no: "फ़ोन नंबर",
      add_row: "खाली पंक्तियाँ जोड़े",
    },
    labels_Français: {
      group: "Groupes",
      name: "Nom",
      village: "Village",
      person_name: "Nom de la personne",
      father_name: "Nom du père",
      age: "Age",
      gender: "Genre",
      phone_no: "Numéro de téléphone",
      add_row: "ajouter des lignes vides",
    },
    labels_English: {
      group: "Group",
      name: "Name",
      village: "Village",
      person_name: "Person Name",
      father_name: "Father Name",
      age: "Age",
      gender: "Gender",
      phone_no: "Phone No",
      add_row: "Add Empty Rows",
    },
    list_elements_हिन्दी: [
      { header: "आईडी", element: "online_id" },
      { header: "नाम", element: "group_name" },
      { header: "गाँव", element: "village.village_name" },
    ],
    list_elements_Français: [
      { header: "Identité", element: "online_id" },
      { header: "Nom", element: "group_name" },
      { header: "Village", element: "village.village_name" },
    ],
    list_elements_English: [
      { header: "ID", element: "online_id" },
      { header: "Name", element: "group_name" },
      { header: "Village", element: "village.village_name" },
    ],
    add_template_name: "group_add_edit_template",
    edit_template_name: "group_add_edit_template",
    rest_api_url: "/coco/api/v2/group/",
    entity_name: "group",
    inc_table_name: "persongroup",
    unique_together_fields: ["group_name", "village.id"],
    sort_field: "group_name",
    foreign_entities: {
      village: {
        village: {
          placeholder: "id_village",
          name_field: "village_name",
        },
      },
    },
    inline: {
      entity: "person",
      default_num_rows: 10,
      add_row: 5,
      template: "person_inline",
      joining_attribute: {
        host_attribute: ["id", "group_name"],
        inline_attribute: "group",
      },
      header: "person_inline_header",
      borrow_attributes: [
        {
          host_attribute: "village",
          inline_attribute: "village",
        },
      ],
      foreign_entities: {
        //used at convert_namespace, denormalize only
        village: {
          village: {
            placeholder: "id_village",
            name_field: "village_name",
          },
        },
        group: {
          group: {
            placeholder: "id_group",
            name_field: "group_name",
          },
        },
      },
    },
    form_field_validation: {
      ignore: ".donotvalidate",
      rules: {
        group_name: {
          required: true,
          minlength: 2,
          maxlength: 100,
          allowedChar: true,
        },
        village: "required",
      },
      messages: {
        name: {
          required: "Group name is required",
          minlength: "Group name  should contain at least 2 characters",
          maxlength: "Group name should contain at most 100 characters",
          allowedChar:
            "Group name should contain only english and local language characters",
        },
        village: "Village is required",
      },

      highlight: function (element, errorClass, validClass) {
        $(element).parent("div").parent("div").addClass("error");
      },
      unhighlight: function (element, errorClass, validClass) {
        $(element).parent("div").parent("div").removeClass("error");
      },
      errorElement: "span",
      errorClass: "help-inline red-color",
      errorPlacement: function (label, element) {
        element.parent().append(label);
      },
    },
  };
  var screening_configs = {
    page_header: "Screening",
    config_English: "Screenings",
    config_हिन्दी: "दिखाए गए वीडियो",
    config_Français: "Projections",
    labels_हिन्दी: {
      screening: "दिखाए गए वीडियो",
      date: "विडियो दिखने की तिथि",
      start_time: "आरंभ करने की तिथि",
      end_time: "End Time",
      village: "गाँव",
      mediator: "मध्यस्थ",
      videos_screened: "वीडियो जो दिखाया गया",
      groups_attended: "ग्राम संगठन जिन्होने भाग लिया",
      person: "सदस्य",
      questions_asked: "पूछे गये सवाल",
      del: "हटाओ",
      sr_no: "क्रम संख्या",
      person_attended: "सदस्य जिन्होने भाग लिया",
      form_type: "वर्ग",
      parentcategory: "अभिभावक श्रेणी",
      age: "आयु",
      gender: "लिंग",
      category: "वर्ग",
      health_provider_present: "स्वास्थ्य प्रदाता वर्तमान",
      type_of_video: "सभा का प्रकार",
      frontlineworkerpresent: "फ्रंटलाइन कर्मचारी मौजूद है?",
      type_of_venue: "स्थान का प्रकार",
      meeting_topics: "विषय",
    },
    labels_Français: {
      screening: "Projections",
      date: "Date de projection",
      start_time: "Heure de début",
      end_time: "End Time",
      village: "Village",
      mediator: "Disséminateur",
      videos_screened: "Vidéo projectée",
      groups_attended: "Groupe concerné",
      person: "Personne",
      questions_asked: "Questions posées",
      del: "effacer",
      sr_no: "Serie de Numéro",
      person_attended: "Personne",
      parentcategory: "Catégorie",
      age: "Âge",
      gender: "Le genre",
      category: "Catégorie",
      health_provider_present: "Prestataire de santé présent",
      type_of_video: "Type de rassemblement",
      frontlineworkerpresent: "Présent du travailleur?",
      type_of_venue: "Type de lieu",
      meeting_topics: "Les sujets",
    },
    labels_English: {
      screening: "Screening",
      date: "Date",
      start_time: "Start Time",
      end_time: "End Time",
      village: "Village",
      mediator: "mediator",
      videos_screened: "Videos Screened",
      groups_attended: "Groups Attended",
      person: "Person",
      questions_asked: "Questions Asked",
      del: "Delete",
      sr_no: "Sr. No.",
      person_attended: "Person",
      parentcategory: "Category",
      age: "Age",
      gender: "Gender",
      category: "Category",
      health_provider_present: "Health Provider Present",
      type_of_video: "Type of Gathering",
      frontlineworkerpresent: "Frontline worker present?",
      type_of_venue: "Type of Venue",
      meeting_topics: "Topics",
    },
    list_elements_हिन्दी: [
      { header: "आईडी", element: "online_id" },
      { header: "विडियो दिखने की तिथि", element: "date" },
      { header: "मध्यस्थ", element: "animator.name" },
      { header: "गाँव", element: "village.village_name" },
      {
        header: "ग्राम संगठन जिन्होने भाग लिया",
        subelement: "group_name",
        element: "farmer_groups_targeted",
      },
      {
        header: "वीडियो जो दिखाया गया",
        subelement: "title",
        element: "videoes_screened",
      },
    ],
    list_elements_Français: [
      { header: "Identité", element: "online_id" },
      { header: "Date de projection", element: "date" },
      { header: "Disséminateur", element: "animator.name" },
      { header: "Village", element: "village.village_name" },
      {
        header: "Groupe concerné",
        subelement: "group_name",
        element: "farmer_groups_targeted",
      },
      {
        header: "Vidéo projectée",
        subelement: "title",
        element: "videoes_screened",
      },
    ],
    list_elements_English: [
      { header: "ID", element: "online_id" },
      { header: "Screening Date", element: "date" },
      { header: "Mediator", element: "animator.name" },
      { header: "Village", element: "village.village_name" },
      {
        header: "Groups Attended",
        subelement: "group_name",
        element: "farmer_groups_targeted",
      },
      {
        header: "Videos Screened",
        subelement: "title",
        element: "videoes_screened",
      },
    ],
    add_template_name: "screening_add_edit_template",
    edit_template_name: "screening_add_edit_template",
    rest_api_url: "/coco/api/v2/screening/",
    entity_name: "screening",
    list_var_check: "screening",
    fetch_element: "person",
    fetch_child_element: "directbeneficiaries",
    fetch_key_element: "id",
    combination_display_dict: {
      "#id_group": ["#id_parentcategory", "#id_village"],
    },
    show_health_provider_present: 1,
    fetch_element_that_manipulate: "parentcategory",
    field_change_entity_name: "screening",
    reset_element: "#id_group",
    parent_element_to_hide: "health_provider_present",
    parent_element_label_to_hide: "label_health_provider_present",
    inline_var: "category_row7_",
    hide_dict: {
      "th#id_age": "input#age_row7",
      "th#id_category": "div#category_row7_chosen",
      "th#id_gender": "input#gender_row7",
      "#label_health_provider_present": "#id_health_provider_present",
    },
    // 'fields_to_hide': ['input#age_row7, input#gender_row7, div#category_chosen', "div#category_row7_chosen", "#id_health_provider_present"],
    // 'headers_to_hide': ['th#id_age', 'th#id_gender', 'th#id_category', "#label_health_provider_present"],
    parent_id_for_inline: "row7",
    remove_attribute_field: "select#category_row7",
    fields_to_hide_arr_for_hnn: [
      "#label_health_provider_present",
      "#id_health_provider_present",
    ],
    download_chunk_size: 1000,
    unique_together_fields: ["date", "start_time", "village.id", "animator.id"],
    text_to_select_display_hack: true,
    text_to_select_display_hack_field_array: [
      "frontline_worker_present",
      "type_of_venue",
      "type_of_video",
      "meeting_topics",
    ],
    afterSave: function (off_json, Offline) {
      var dfd = new $.Deferred();
      var videos_shown = off_json.videoes_screened;
      console.log("recvd off_json in afterSave - " + JSON.stringify(off_json));
      update_attendees()
        .done(function () {
          dfd.resolve();
        })
        .fail(function () {
          dfd.reject();
        });
      return dfd.promise();

      function update_attendees() {
        var all_update_dfds = [];
        $.each(off_json.farmers_attendance, function (index, per) {
          all_update_dfds.push(update_attendee(per));
        });
        return $.when.apply($, all_update_dfds);
      }

      function update_attendee(per) {
        var p_dfd = new $.Deferred();
        Offline.fetch_object("person", "id", parseInt(per.person_id))
          .done(function (p_model) {
            console.log("old p -" + JSON.stringify(p_model));
            var videos_seen = p_model.get("videos_seen");
            if (videos_seen) {
              var videos_seen_ids = _.pluck(videos_seen, "id");
              $.each(videos_shown, function (index, vid) {
                if ($.inArray(vid.id, videos_seen_ids) == -1)
                  videos_seen.push(vid);
              });
            } else videos_seen = videos_shown;
            p_model.set("videos_seen", videos_seen);
            Offline.save(p_model, "person", p_model.toJSON())
              .done(function (p_model) {
                console.log("new p -" + JSON.stringify(p_model));
                p_dfd.resolve();
              })
              .fail(function (error) {
                console.log("error updating person in after save - " + error);
                p_dfd.reject(error);
              });
          })
          .fail(function (error) {
            console.log("error fetching person in after save - " + error);
            p_dfd.reject(error);
          });
        return p_dfd;
      }
    },
    foreign_entities: {
      village: {
        village: {
          placeholder: "id_village",
          name_field: "village_name",
        },
      },

      parentcategory: {
        parentcategory: {
          placeholder: "id_parentcategory",
          name_field: "parent_category_name",
        },
      },

      video: {
        videoes_screened: {
          placeholder: "id_videoes_screened",
          name_field: "title",
          dependency: [
            {
              source_form_element: "parentcategory",
              dep_attr: "parent_category",
              parent_attr: "category",
              forced_filter_attr: "category_name",
            },
          ],
        },
      },

      frontlineworkerpresent: {
        frontlineworkerpresent: {
          placeholder: "id_frontlineworkerpresent",
          name_field: "worker_type",
        },
      },

      mediator: {
        animator: {
          placeholder: "id_animator",
          name_field: "name",
          dependency: [
            {
              source_form_element: "village",
              dep_attr: "assigned_villages",
            },
          ],
        },
      },
      group: {
        farmer_groups_targeted: {
          placeholder: "id_group",
          name_field: "group_name",
          dependency: [
            {
              source_form_element: "village",
              dep_attr: "village",
            },
          ],
        },
      },
      person: {
        person: {
          placeholder: "id_person",
          name_field: "person_name",
          name_field_father_name: "father_name",
          name_field_extra_info: "group",
          name_field_group_name: "group_name",
          name_field_person_id: "online_id",

          dependency: [
            {
              source_form_element: "village",
              dep_attr: "village",
            },
          ],
        },
        farmers_attendance: {
          dependency: [
            {
              source_form_element: "farmer_groups_targeted",
              dep_attr: "group",
            },
            {
              source_form_element: "person",
              dep_attr: "id",
            },
          ],
          id_field: "person_id", // for convert_namespace conversion
          expanded: {
            // won't be denormalised, wud be converted offline to online, render wud use a template declared and nt options template, any field to be denormalised or converted offline to online can be declared - this shd be clubbed and put as foreign entity of expanded.
            template: "person_pma_template",
            placeholder: "pmas",
            denormalize: {
              // any field in expanded template to be denormalised
              expressed_adoption_video: {
                name_field: "title",
              },
            },
            foreign_entities: {
              // any more field in expanded template for offline to online conv
              video: {
                expressed_adoption_video: {
                  entity_name: "video",
                  name_field: "title",
                },
              },
            },
            extra_fields: [
              "category",
              "expressed_question",
              "interested",
              "expressed_adoption_video",
            ],
          },
        },
      },
    },
    form_field_validation: {
      ignore: [],
      rules: {
        date: {
          required: true,
          validateDate: true,
        },
        start_time: {
          required: true,
          validateTime: true,
        },
        animator: "required",
        village: "required",
        videoes_screened: "required",
        farmer_groups_targeted: "required",
      },
      messages: {
        date: {
          required: "Screening date is required",
          validateDate: "Enter screening date in the form of YYYY-MM-DD",
        },
        start_time: {
          required: "Screening start time is required",
          validateTime:
            "Enter the start time in the form of HH:MM. Use 24 hour format",
        },
        animator: "Mediator is required",
        village: "Village is required",
        videoes_screened: "Videos screened is required",
        farmer_groups_targeted: "Groups attended is required",
      },

      highlight: function (element, errorClass, validClass) {
        $(element).parent("div").parent("div").addClass("error");
      },
      unhighlight: function (element, errorClass, validClass) {
        $(element).parent("div").parent("div").removeClass("error");
      },
      errorElement: "span",
      errorClass: "help-inline red-color",
      errorPlacement: function (label, element) {
        element.parent().append(label);
      },
    },
  };

  var adoption_configs = {
    page_header: "Adoption",
    config_English: "Adoptions",
    config_हिन्दी: "अपनाए हुए विधि",
    config_Français: "Adoptions",
    labels_हिन्दी: {
      adoption: "अपनाए हुए विधि",
      village: "गाँव",
      mediator: "मध्यस्थ",
      video: "वीडियो",
      groups_attended: "ग्राम संगठन जिन्होने भाग लिया ",
      person: "सदस्य",
      del: "हटाओ",
      sr_no: "क्रम संख्या",
      date_of_adoption: "अपनाने की तारीख",
      date_of_verification: "अपनाने के जाँच की तारीख",
      member_adopt_second: "क्या लाभार्थी व्यवहार 2 का अभ्यास कर रहा है?",
      member_adopt: "क्या सदस्य ने क्रिया अपनाई",
      recall_nonnegotiable: "क्या सदस्य ने अति आवश्यक बातो को याद किया था",
      parentcategory: "वर्ग",
    },
    labels_Français: {
      adoption: "Adoptions",
      village: "Village",
      mediator: "Disséminateur",
      video: "Vidéo",
      groups_attended: "Groupes concernés",
      person: "Personne",
      del: "effacer",
      sr_no: "Serie de Numéro",
      date_of_adoption: "Date d'adoption",
      date_of_verification: "Date de vérification",
      member_adopt_second: "Le bénéficiaire exerce-t-il le comportement2?",
      member_adopt: "membre at-il adopté la pratique",
      recall_nonnegotiable: "Le député at rappeler les points non négociables",
      parentcategory: "Catégorie",
    },
    labels_English: {
      adoption: "Adoption",
      village: "Village",
      mediator: "Mediator",
      video: "Video",
      groups_attended: "Groups Attended",
      person: "Person",
      del: "Delete",
      sr_no: "Sr. No.",
      video: "Video",
      date_of_adoption: "Date of Adoption",
      date_of_verification: "Date of Verification",
      member_adopt_second: "Is the beneficiary practicing the behavior2?",
      member_adopt: "Did member adopt the practice",
      recall_nonnegotiable: "Did the member recall non-negotiable points",
      parentcategory: "Category",
    },
    list_elements_हिन्दी: [
      { header: "आईडी", element: "online_id" },
      { header: "अपनाने की तारीख", element: "date_of_adoption" },
      { header: "सदस्य कि आईडी", element: "person.online_id" },
      { header: "सदस्य", element: "person.person_name" },
      { header: "ग्राम संगठन का नाम", element: "group.group_name" },
      { header: "गाँव", element: "village.village_name" },
      { header: "वीडियो", element: "video.title" },
    ],
    list_elements_Français: [
      { header: "Identité", element: "online_id" },
      { header: "Date de vérification", element: "date_of_adoption" },
      { header: "Personne Identité", element: "person.online_id" },
      { header: "Personne", element: "person.person_name" },
      { header: "Groupe/groupement", element: "group.group_name" },
      { header: "Village", element: "village.village_name" },
      { header: "Vidéo", element: "video.title" },
    ],
    list_elements_English: [
      { header: "ID", element: "online_id" },
      { header: "Verification Date", element: "date_of_adoption" },
      { header: "Person ID", element: "person.online_id" },
      { header: "Person", element: "person.person_name" },
      { header: "Group", element: "group.group_name" },
      { header: "Village", element: "village.village_name" },
      { header: "Video", element: "video.title" },
    ],
    add_template_name: "adoption_add_template",
    edit_template_name: "adoption_edit_template",
    rest_api_url: "/coco/api/v2/adoption/",
    entity_name: "adoption",
    list_var_check: "adoption",
    show_health_provider_present: 1,
    fetch_element_that_manipulate: "parentcategory",

    // 'field_change_entity_name': "adoption",
    // 'combination_display_field': '#id_group',
    // 'combination_display_field_with_value': ['#id_parentcategory', '#id_village'],

    combination_display_dict: {
      "#id_group": ["#id_parentcategory", "#id_village"],
    },

    // 'parent_element_to_hide': 'adopt_practice_chosen',
    // 'parent_element_label_to_hide': 'label_id_member_adopt',
    fetch_key_element: "id",
    remove_attribute_field: "adopt_practice",
    hide_dict: {
      "th#id_member_adopt": "div#id_adopt_practice",
      "th#id_label_recall_nonnegotiable": "div#id_recall_nonnegotiable",
      "#label_health_provider_present": "#id_health_provider_present",
    },
    reset_element: "#id_group",
    inc_table_name: "personadoptpractice",
    unique_together_fields: ["person.id", "video.id", "date_of_adoption"],
    text_to_select_display_hack: true,
    text_to_select_display_hack_field_id: "adopt_practice",
    text_to_select_display_hack_field_array: ["adopt_practice_second"],
    inline_headers_for_hide_show_arr: [
      "th#id_member_adopt",
      "th#id_recall_nonnegotiable",
      "td#id_recall_nonnegotiable",
      "th#id_member_adopt",
    ],
    form_field_validation: {
      ignore: [],
      rules: {
        person: {
          required: true,
        },
        video: {
          required: true,
        },
        animator: {
          required: true,
        },
        date_of_adoption: {
          required: true,
          validateDate: true,
        },
      },
      messages: {
        person: {
          required: "person is required",
        },
        video: {
          required: "video is required",
        },
        animator: {
          required: "Mediator is required",
        },
        date_of_adoption: {
          required: "Date of Adoption is required",
        },
      },
      highlight: function (element, errorClass, validClass) {
        $(element).parent("div").parent("div").addClass("error");
      },
      unhighlight: function (element, errorClass, validClass) {
        $(element).parent("div").parent("div").removeClass("error");
      },
      errorElement: "span",
      errorClass: "help-block red-color",
      errorPlacement: function (label, element) {
        element.parent().append(label);
      },
      display: "block",
    },
    add: {
      foreign_entities: {
        village: {
          village: {
            placeholder: "id_village",
            name_field: "village_name",
          },
        },

        parentcategory: {
          parentcategory: {
            placeholder: "id_parentcategory",
            name_field: "parent_category_name",
          },
        },

        video: {
          video: {
            placeholder: "id_video",
            name_field: "title",
            dependency: [
              {
                source_form_element: "parentcategory",
                dep_attr: "parent_category",
                parent_attr: "category",
              },
            ],
          },
        },

        group: {
          group: {
            placeholder: "id_group",
            name_field: "group_name",
            dependency: [
              {
                source_form_element: "village",
                dep_attr: "village",
              },
            ],
          },
        },
        mediator: {
          animator: {
            placeholder: "id_animator",
            name_field: "name",
            dependency: [
              {
                source_form_element: "village",
                dep_attr: "assigned_villages",
              },
            ],
          },
        },
        person: {
          float_person: {
            placeholder: "id_person",
            name_field: "person_name",
            name_field_father_name: "father_name",
            name_field_extra_info: "group",
            name_field_group_name: "group_name",
            name_field_person_id: "online_id",
            dependency: [
              {
                source_form_element: "village",
                dep_attr: "village",
              },
            ],
          },
          farmers_attendance: {
            dependency: [
              {
                source_form_element: "group",
                dep_attr: "group",
              },
              {
                source_form_element: "float_person",
                dep_attr: "id",
              },
            ],
            filter_dependency: [
              {
                source_form_element: "video",
                dep_attr: "videos_seen",
              },
            ],
            id_field: "person_id", // for convert_namespace conversion
            expanded: {
              // won't be denormalised, wud be converted offline to online, render wud use a template declared and nt options template, any field to be denormalised or converted offline to online can be declared - this shd be clubbed and put as foreign entity of expanded.
              template: "adoption_inline",
              placeholder: "bulk",
            },
          },
        },
      },
      bulk: {
        foreign_fields: {
          //foreign fields in the individual objects
          video: {
            video: {
              name_field: "title",
            },
          },
          person: {
            person: {
              name_field: "person_name",
            },
          },
          village: {
            village: {
              name_field: "village_name",
            },
          },
          group: {
            group: {
              name_field: "group_name",
            },
          },
          mediator: {
            animator: {
              name_field: "name",
            },
          },
          parentcategory: {
            parentcategory: {
              name_field: "parent_category_name",
            },
          },
        },
        borrow_fields: [
          "village",
          "group",
          "video",
          "animator",
          "parentcategory",
        ],
      },
    },
    edit: {
      foreign_entities: {
        village: {
          village: {
            placeholder: "id_village",
            name_field: "village_name",
          },
        },
        person: {
          person: {
            placeholder: "id_person",
            name_field: "person_name",
          },
        },

        parentcategory: {
          parentcategory: {
            placeholder: "id_parentcategory",
            name_field: "parent_category_name",
          },
        },

        video: {
          video: {
            placeholder: "id_video",
            // 'sub_attr': 'videos_seen',
            name_field: "title",
            dependency: [
              {
                source_form_element: "person",
                dep_attr: "id",
                src_attr: "videos_seen",
              },
            ],
          },
        },
        mediator: {
          animator: {
            placeholder: "id_animator",
            name_field: "name",
            dependency: [
              {
                source_form_element: "village",
                dep_attr: "assigned_villages",
              },
            ],
          },
        },
      },
    },
  };

  var person_configs = {
    page_header: "Person",
    config_English: "Persons",
    config_हिन्दी: "सदस्य",
    config_Français: "Personnes",
    labels_हिन्दी: {
      person: "सदस्य",
      name: "नाम",
      father_name: "पिता/पति का नाम",
      village: "गाँव",
      gender: "लिंग",
      age: "आयु",
      phone_no: "फ़ोन नंबर",
      group: "ग्राम संगठन का नाम",
      is_modelfarmer: "मॉडल किसान",
    },
    labels_Français: {
      person: "Personnes",
      name: "Nom de la personne",
      father_name: "Nom du père",
      village: "Nom du village",
      gender: "Genre",
      age: "Age",
      phone_no: "Numéro de téléphone",
      group: "Groupe",
      is_modelfarmer: "Modèle Agriculteur",
    },
    labels_English: {
      person: "Person",
      name: "Name",
      father_name: "Father Name",
      village: "Village",
      gender: "Gender",
      age: "Age",
      phone_no: "Phone Number",
      group: "Group",
      is_modelfarmer: "Model Farmer",
    },
    list_elements_हिन्दी: [
      { header: "आईडी", element: "online_id" },
      { header: "सदस्य का नाम", element: "person_name" },
      { header: "पिता/पति का नाम", element: "father_name" },
      { header: "गाँव", element: "village.village_name" },
      { header: "ग्राम संगठन का नाम", element: "group.group_name" },
    ],
    list_elements_Français: [
      { header: "Identité", element: "online_id" },
      { header: "Nom de la personne", element: "person_name" },
      { header: "Nom du père", element: "father_name" },
      { header: "Nom du village", element: "village.village_name" },
      { header: "Groupe", element: "group.group_name" },
    ],
    list_elements_English: [
      { header: "ID", element: "online_id" },
      { element: "person_name" },
      { element: "father_name" },
      { element: "village.village_name" },
      { element: "group.group_name" },
    ],
    add_template_name: "person_add_edit_template",
    edit_template_name: "person_add_edit_template",
    rest_api_url: "/coco/api/v2/person/",
    entity_name: "person",
    foreign_entities: {
      village: {
        village: {
          placeholder: "id_village",
          name_field: "village_name",
        },
      },
      group: {
        group: {
          placeholder: "id_group",
          name_field: "group_name",
          dependency: [
            {
              source_form_element: "village",
              dep_attr: "village",
            },
          ],
        },
      },
    },
    // unique_together_fields: ["person_name", "father_name", "village.id"],
    sort_field: "person_name",
    form_field_validation: {
      ignore: [],
      rules: {
        person_name: {
          required: true,
          minlength: 2,
          maxlength: 100,
          // allowedChar:true
        },

        father_name: {
          // required: true,
          minlength: 2,
          maxlength: 100,
          // allowedChar:true
        },
        age: {
          digits: true,
          min: 10,
          max: 99,
        },
        gender: "required",
        phone_no: {
          digits: true,
          minlength: 10,
          maxlength: 10,
        },
        village: {
          required: true,
        },
      },
      messages: {
        person_name: {
          required: "Person name is required",
          minlength: "Person name  should contain at least 2 characters",
          maxlength: "Person Name should contain at most 100 characters",
          allowedChar:
            "Person name should contain only english and local language characters",
        },
        father_name: {
          required: "Father's name is required",
          minlength: "Father's name should contain at least 2 characters",
          maxlength: "Father's name should contain at most 100 characters",
          allowedChar:
            "Father's name should contain only english and local language characters",
        },
        age: {
          digits: "Age should contain only digits",
          min: "Age should not be less than 10 year",
          max: "Age should not be less than 100 years",
        },
        gender: {
          required: "Gender is required",
        },
        phone_number_person: {
          digits: "Phone number should contain digits only",
          maxlength: "Phone number should not contain more than 10 digits",
        },
        village: {
          required: "Village is required",
        },
      },

      highlight: function (element, errorClass, validClass) {
        $(element).parent("div").parent("div").addClass("error");
      },
      unhighlight: function (element, errorClass, validClass) {
        $(element).parent("div").parent("div").removeClass("error");
      },
      errorElement: "span",
      errorClass: "help-inline red-color",
      errorPlacement: function (label, element) {
        element.parent().append(label);
      },
    },
  };

  var misc = {
    download_chunk_size: 2000,
    data_transfer_schema: "uploadqueue",
    agg_variable: "2",
    health_variable: "1",
    variable_dict: { agg_variable: "2", health_variable: "1" },
    data_transfer_credentials_schema: "user",
    languages: ["हिन्दी", "English", "Français"],
    ethiopia_partners: ["moa-dg ethiopia", "ide", "oa", "saa"],
    health_variable: "1",
    agg_variable: "2",
    upavan_variable: "3",
    menu_options_to_hide: {
      ".ahnn": "ahnn",
      ".hnn": ".hnn",
      "li.hnn": "li.hnn",
    },
    upavan_user_fields: [
      "#type_of_venue",
      "#type_of_video",
      "#frontlineworkerpresent",
      "#end_time",
      "#remove-table",
      "#srf-1",
      "#srf-2",
    ],
    label_upavan_dict: {
      "#id_label_animator": "CSP name",
      "#id_label_videos_screened": "Video Name",
      "#id_category": "Beneficiary",
      "#id_dob": "Date of Home Visit",
      ".non": "Beneficiary recalled the knowledge recall point?",
      "th#id_member_adopt": "Is the beneficiary practicing the behavior1?",
      "#non_nego": "Knowledge Recall Points",
    },
    label_dict: {
      "#id_label_animator": "Mediator",
      "#id_label_videos_screened": "Videos Screened",
      "#id_category": "Category",
      "#id_dob": "Date of Verification",
      ".non": "Beneficiary recalled the knowledge recall point?",
      "#id_member_adopt": "Is the beneficiary practicing the behavior ?",
      "#non_nego": "Non Negotiables",
    },
    inline_upavan_label_dict: {
      "th#id_label_recall_nonnegotiable":
        "Did the member recall the knowledge recall points ?",
      "th#id_member_adopt": "Is the beneficiary practicing the behavior1 ?",
      "#id_dob": "Date of Home Visit",
      "th#non_nego": "Knowledge Recall Points",
    },
    inline_label_dict: {
      "th#id_label_recall_nonnegotiable":
        "Did the member recall the non negotiable ?",
      "th#id_member_adopt": "Did member adopt the practice? ?",
      "#id_dob": "Date of Verification",
      "th#non_nego": "Non Negotiables",
    },
    element_to_be_hidden_for_upavan: {
      "#id_meeting_topic": "#id_meeting_topic",
    },
    inline_var_to_be_hidden: {
      "th#phy": "td#phy_check",
      "th#id_member_adopt_second": "td#id_adopt_practice_second",
    },
    meta_default: "English",
    meta_English: {
      stop: "Stop",
      close: "close",
      sync: "Sync",
      export: "Export Data",
      save: "Save and Add Another",
      help: "Help",
      logout: "Logout",
      download: "Downloading...",
      upload: "Uploading...",
      inprogress: "In Progress",
      done: "Done",
      edit: "Edit",
      delete_download: "Delete and Download Database",
      save_again: "Save Again",
      discard: "Discard",
      upload_total: "Data items to be uploaded",
      upload_done: "Data Uploaded",
      upload_pending: "Data pending to be uploaded",
      error: "Error!!",
      upload_error: "Internet connectivity lost. Please try after sometime!",
      copy_clipboard: "Copy to clipboard",
      excel_download: "Download in excel",
      search: "Search: ",
      enteries: "Enteries: ",
      total_enteries: "Total Enteries: ",
      next: "Next",
      previous: "Previous",
      list_page_help:
        "For multiple column sorting, press and hold the shift key while sorting each column.",
      line_1: "Welcome to COCO",
      line_2:
        "COCO helps you to seamlessly enter data in conditions of intermittent connectivity.",
      line_3: "Add data",
      line_4:
        "To add some data, click on (+) sign next to the type of data that you want to add.",
      line_5: "View Data",
      line_6:
        "To view, sort and search through your data, click on the data link in the sidebar.",
      line_7: "Sync data",
      line_8:
        "To sync data with the server, click on the sync button. While syncing, if some data is rejected by the server, you will get the opportunity to correct the data, or in case of duplicate entries, to discard it. The number in the button shows how many entries are yet to be uploaded. Clicking on the sync button will also download the database if it is not completely downloaded.",
      line_9: "We value your feedback",
      line_10:
        "Do share your feedback by mailing us at <a href='mailto:system@digitalgreen.org'>system@digitalgreen.org</a>",
      line_11: "Database last deleted and downloaded at",
      line_12: "Database last synced at",
      line_13: "Entries to upload",
    },
    meta_हिन्दी: {
      stop: "रोकें",
      close: "बंद करें",
      sync: "सिंक करें",
      export: "डाटा डाउनलोड करें",
      save: "एक और जोड़े",
      help: "हेल्प",
      logout: "लोग आउट",
      download: "डाउनलोड हो रहा है...",
      upload: "अपलोड हो रहा है...",
      inprogress: "कार्य प्रगति में है",
      done: "कार्य समाप्त हो गया है",
      edit: "बदलें",
      delete_download: "पुराना डेटा हटाएँ और नया जोड़ें ",
      save_again: "फिर से जोड़े",
      discard: "हटाये",
      upload_total: "अपलोड के लिए कुल डेटा",
      upload_done: "डेटा अपलोड हो गया है",
      upload_pending: "डेटा अपलोड होना बाकी है",
      error: "त्रुटि!!",
      upload_error:
        "अभी इंटरनेट की सुविधा नही है। कृपया कुछ देर बाद प्रयास करें!",
      copy_clipboard: "क्लिपबोर्ड पर कॉपी करें",
      excel_download: "एक्सेल में डाउनलोड करें",
      search: "खोजें: ",
      enteries: "डेटा: ",
      total_enteries: "कुल डेटा: ",
      next: "अगला",
      previous: "पिछला",
      list_page_help:
        "एक से जादा श्रेणी के डेटा को क्रम मे लाने के लिए एक से अधिक श्रेणी चुनते समय शिफ्ट बटन दबाए रख़े",
      line_1: "आपका COCO मे स्वागत है",
      line_2: "COCO आपको अनिरंतर इंटरनेट में भी डेटा जोड़ने में मदद करता है",
      line_3: "डेटा जोड़े",
      line_4:
        "जो डेटा जोड़ना है उसके बगल में डेटा जोड़ने के लिए (+) पर क्लिक करें",
      line_5: "डेटा देखें",
      line_6:
        "डेटा देखने, खोजने और क्रम में लाने के लिए, बाँई तरफ उनके नाम पे क्लिक करें",
      line_7: "डेटा सिंक करें",
      line_8:
        "डेटा सिंक करने के लिए सिंक बटन पर क्लिक करें। सिंक करते समय अगर डेटा किसी कारण अपलोड नहीं हो रहा है तोह आपको डेटा सुधरने या अगर दोहरा डेटा है तो डेटा हटाने का मौका मिलेगा। सिंक बटन पर जो संख्या है वह ये बताता है की कितना डेटा अभी अपलोड करना बाकी है। सिंक बटन पे क्लिक करने पर अगर डेटा डाउनलोड नहीं हुआ है तोह डेटा पूरा डाउनलोड हो जाएगा।",
      line_9: "हम आपके सुझाव का मूल्य समझते हैं",
      line_10:
        "अपने सुझाव हमें <a href='mailto:system@digitalgreen.org'>system@digitalgreen.org</a> पर भेजें",
      line_11: "पिछली बार डेटा हटाया और जोड़ा गया था",
      line_12: "पिछली बार डेटा सिंक हुआ था",
      line_13: "अपलोड करने वाले प्रविष्टियों",
    },
    meta_Français: {
      stop: "Arrêtez",
      close: "Fermer",
      sync: "Sync",
      export: "Télécharger des données",
      save: "Enregistrer",
      help: "Aidez-moi",
      logout: "Se déconnecter",
      download: "Téléchargement en cours...",
      upload: "L'ajout...",
      inprogress: "En cours",
      done: "Terminé",
      edit: "modifier",
      delete_download: "Supprimer et télécharger la base de données",
      save_again: "Enregistrer à nouveau",
      discard: "Jeter",
      upload_total: "Les éléments de données à être téléchargées",
      upload_done: "Les données téléchargées",
      upload_pending: "Données en attente d' être téléchargées",
      error: "Erreur!!",
      upload_error:
        "Connectivité Internet perdue. Essayez après un certain temps!",
      copy_clipboard: "Copier dans le presse-papier",
      excel_download: "Télécharger Excel",
      search: "Chercher: ",
      enteries: "Entrées: ",
      total_enteries: "Entrées totales: ",
      next: "Prochain",
      previous: "Précédent",
      list_page_help:
        "Pour le tri de plusieurs colonnes, appuyez et maintenez la touche Maj enfoncée tout en triant chaque colonne",
      line_1: "Bienvenu dans COCO",
      line_2:
        "COCO vous aide à saisir de façon transparente des données dans des conditions de connectivité intermittente",
      line_3: "Ajouter des données",
      line_4:
        "Pour ajouter des données, cliquez sur (+) cochez à côté du type de données que vous souhaitez ajouter",
      line_5: "Voir les données",
      line_6:
        "Pour afficher, trier et rechercher dans vos données, cliquez sur le lien de données dans la barre latérale",
      line_7: "Synchroniser les données",
      line_8:
        "Pour synchroniser des données avec le serveur, cliquez sur le bouton de synchronisation. Pendant la synchronisation, si certaines données sont rejetées par le serveur, vous aurez la possibilité de les corriger , ou en cas d'entrées en double. Le nombre dans le bouton indique le nombre d'entrées qui ne sont pas encore téléchargées. En cliquant sur le bouton de synchronisation, il sera également téléchargé la base de données si elle n'est pas complètement téléchargée.",
      line_9: "Nous apprécions vos commentaires",
      line_10:
        "Envoyez nous vos commentaires par courriel à <a href='mailto:system@digitalgreen.org'>system@digitalgreen.org</a>",
      line_11: "Base de données dernièrement supprimée et téléchargée ici",
      line_12: "Base de données dernièrement synchronisée",
      line_13: "Entrées pour téléchargement",
    },
    background_download_interval: 5 * 60 * 1000,
    inc_download_url: "/coco/get_log/",
    afterFullDownload: function (start_time, download_status) {
      return saveTimeTaken();
      function saveTimeTaken() {
        var record_endpoint = "/coco/record_full_download_time/";
        return $.post(record_endpoint, {
          start_time: start_time,
          end_time: new Date().toJSON().replace("Z", ""),
        });
      }
    },
    reset_database_check_url: "/coco/reset_database_check/",
    onLogin: function (Offline, Auth) {
      getLastDownloadTimestamp().done(function (timestamp) {
        askServer(timestamp);
      });
      var that = this;
      function askServer(timestamp) {
        $.get(that.reset_database_check_url, {
          lastdownloadtimestamp: timestamp,
        }).done(function (resp) {
          console.log(resp);
          if (resp == "1") {
            alert(
              "Your database will be redownloaded because of some changes in data."
            );
            Offline.reset_database();
          }
        });
      }
      function getLastDownloadTimestamp() {
        var dfd = new $.Deferred();
        Offline.fetch_object("meta_data", "key", "last_full_download_start")
          .done(function (model) {
            dfd.resolve(model.get("timestamp"));
          })
          .fail(function (model, error) {});
        return dfd;
      }
    },
  };

  return {
    village: village_configs,
    mediator: mediator_configs,
    directbeneficiaries: directbeneficiaries_configs,
    video: video_configs,
    group: group_configs,
    person: person_configs,
    screening: screening_configs,
    adoption: adoption_configs,
    language: language_configs,
    tag: tag_configs,
    category: category_configs,
    parentcategory: parent_category_configs,
    subcategory: subcategory_configs,
    videopractice: videopractice_configs,
    district: district_configs,
    nonnegotiable: nonnegotiable_configs,
    frontlineworkerpresent: frontlineworkerpresent_configs,
    misc: misc,
  };
});
