/**
 * Created by Abhishek Lodha on 2016-08-19.
 */

function filter_villages_from_selected_districct() {
    jQuery("#id_district").change(function() {
        if (jQuery("#id_district").val() != 0) {
            var district_id = jQuery("#id_district").val();
            jQuery.get("/coco/filter_villages/", {
                    'district_id': district_id
                })
                .done(function(data) {
                    console.log(data);
                    var json_data = JSON.parse(data);
                    villages = json_data.villages;
                    // console.log(villages);
                    var villages_length = villages.length;
                    var options = [];
                    options.push('<select multiple="multiple" class="selectfilter" name="villages" id="id_villages">');
                    for (var i = 0; i < villages_length; i++) {
                        options.push('<option value="' + villages[i]['id'] + '">' +
                            villages[i]['village_name'] + ' (' + villages[i]['block__block_name'] + ')' + '</option>');
                    }
                    options.push('</select>');
                    jQuery('#id_villages').html(options.join(''));

                    // var title = $('#id_instalation option:selected"').text().toLowerCase();
                    SelectFilter.init(null, "Available Villages", 0, "/path/to/django/media/");

                });
        }
    });
}

window.onload = filter_villages_from_selected_districct;
