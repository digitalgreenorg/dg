function filter()
{

        if($("#id_village").val()>0)
        {

                $.getJSON("/animators-by-village-id/"+$("#id_village").val()+"/", function(j)
                {
                        var options = '<option value="">---------- </option>';
                        for (var i = 0; i < j.length; i++)
                        {
                          options += '<option value="' + parseInt(j[i].pk) + '">' + j[i].fields['name'] + '</option>';
                        }
                        $("#id_animators_trained").html(options);
                        $("#id_animators_trained option:first").attr('selected', 'selected');
                        $("#id_animators_trained").attr('disabled', false);
                })

        }
}
