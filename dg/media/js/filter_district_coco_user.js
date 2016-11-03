/**
 * Created by Abhishek Lodha on 2016-08-19.
 */

function filter_villages_from_selected_districct() {
  // Sele
  // SelectBox.move("id_villages_from","id_villages_to");
  // SelectFilter.refresh_icons("id_villages");

  jQuery.get("/coco/filter_villages/", {
          'district_id': 41265757
      })
      .done(function(data) {
          console.log(data);
          var json_data = JSON.parse(data);
          villages = json_data.villages;
          // console.log(villages);
          var villages_length = villages.length;
          var options = [];
          // options.push('<select multiple="multiple" class="selectfilter" name="villages" id="id_vill">');
          for (var i = 0; i < villages_length; i++) {
              options.push('<option value="' + villages[i]['id'] + '">' +
                  villages[i]['village_name'] + ' (' + villages[i]['block__block_name'] + ')' + '</option>');
          }
          // options.push('</select>');
          jQuery('#id_villages_from').html(options.join(''));

          // SelectFilter.init("id_villages_from", "Villages", 1, "/media/admin/");
          SelectBox.init("id_villages_from");

      });


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
                    // options.push('<select multiple="multiple" class="selectfilter" name="villages" id="id_vill">');
                    for (var i = 0; i < villages_length; i++) {
                        options.push('<option value="' + villages[i]['id'] + '">' +
                            villages[i]['village_name'] + ' (' + villages[i]['block__block_name'] + ')' + '</option>');
                    }
                    // options.push('</select>');
                    jQuery('#id_villages_from').html(options.join(''));

                    // SelectFilter.init("id_villages_from", "Villages", 1, "/media/admin/");
                    SelectBox.init("id_villages_from");
                });
        }
    });
}

window.onload = filter_villages_from_selected_districct;
