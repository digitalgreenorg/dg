
function CustomFileBrowser(field_name, url, type, win) {
    tinyMCE.activeEditor.windowManager.open({
        file: window.__filebrowser_url + '?pop=2&type=' + type,
        width: 820,  // Your dimensions may differ - toy around with them!
        height: 500,
        resizable: "yes",
        scrollbars: "yes",
        inline: "yes",  // This parameter only has an effect if you use the inlinepopups plugin!
        close_previous: "no"
    }, {
        window: win,
        input: field_name,
        editor_id: tinyMCE.selectedInstance.editorId
    });
    return false;
}

jQuery(function($) {

    if (typeof tinyMCE != 'undefined') {

        tinyMCE.init({

            // main settings
            mode : "specific_textareas",
            editor_selector : "mceEditor",
            theme: "advanced",
            language: "en",
            dialog_type: "window",
            editor_deselector : "mceNoEditor",
            skin: "default",

            // general settings
            width: '800px',
            height: '450px',
            indentation : '10px',
            fix_list_elements : true,
            remove_script_host : true,
            accessibility_warnings : false,
            object_resizing: false,
            //cleanup: false, // SETTING THIS TO FALSE WILL BREAK EMBEDDING YOUTUBE VIDEOS
            forced_root_block: "p",
            remove_trailing_nbsp: true,

            external_link_list_url: '/displayable_links.js',
            relative_urls: false,
            convert_urls: false,

            // callbackss
            file_browser_callback: "CustomFileBrowser",

            // theme_advanced
            theme_advanced_toolbar_location: "top",
            theme_advanced_toolbar_align: "left",
            theme_advanced_statusbar_location: "",
            theme_advanced_buttons1: "bold,italic,|,link,unlink,|,image,|,media,charmap,|,code,|,table,|,bullist,numlist,blockquote,|,undo,redo,|,styleselect,|,search,replace,|,fullscreen,",
            theme_advanced_buttons2: "",
            theme_advanced_buttons3: "",
            theme_advanced_path: false,
            theme_advanced_blockformats: "p,h1,h2,h3,h4,pre",
            theme_advanced_styles: "Heading 1=hdg-a layout-vr-sm; Heading 2=hdg-b layout-vr-sm; Heading 3=hdg-c layout-vr-sm; Heading 4=hdg-e layout-vr-sm; [p] space=copy-para; [img] Right Margin=img; [img] Left Margin=grid-pad-lt-sm; Bullet=bullet-list",
            theme_advanced_resizing : true,
            theme_advanced_resize_horizontal : false,
            theme_advanced_resizing_use_cookie : true,
//            theme_advanced_styles: "Image left-aligned=img_left;Image left-aligned (nospace)=img_left_nospacetop;Image right-aligned=img_right;Image right-aligned (nospace)=img_right_nospacetop;Image Block=img_block",
            advlink_styles: "intern=internal;extern=external",

            // plugins
            plugins: "inlinepopups,contextmenu,tabfocus,searchreplace,fullscreen,advimage,advlink,paste,media,table",
            advimage_update_dimensions_onchange: true,

            // remove MS Word's inline styles when copying and pasting.
            paste_remove_spans: true,
            paste_auto_cleanup_on_paste : true,
            paste_remove_styles: true,
            paste_remove_styles_if_webkit: true,
            paste_strip_class_attributes: true,

            // don't strip anything since this is handled by bleach
            valid_elements: "+*[*]",
            valid_children: "+button[a]",

            content_css: window.__tinymce_css

    	});

    }

});
