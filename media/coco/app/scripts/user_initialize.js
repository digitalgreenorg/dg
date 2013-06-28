define([
    'jquery',
    'form_field_validator'
  ], function(){
    
    var run = function(){
        $.validator.addMethod('allowedChar',
            validateUniCodeChars, 'Enter a string.'
        );
        $.validator.addMethod('validateDate',
            validateDate, 'Enter the date in the format of yyyy-mm-dd.'
        );
        $.validator.addMethod('validateTime',
            validateTime, 'Enter the time in the format of hh:mm in 24 hours format'
        );
		$.validator.addMethod('startBeforeEnd',
            startBeforeEnd, 'End time should be later than start time'
        );
		$.validator.addMethod('dateOrder',
            dateOrder, 'End date should be later than start date'
        );
    }  
    
    function validateUniCodeChars(value) {
    	if(value) {
    		var alphabetCharset = /^[a-zA-Z ]+$/;
    		var strictUniCodeChars = /.*[^\\x20-\\x7E].*/;
    		if(alphabetCharset.test(value)) {
    			return true;
    		} 
    		if(strictUniCodeChars.test(value)) {
    			return true;
    		} else {
    			return false;
    		}
    	} else {
    		return true;
    	}
    }

    function validateDate(value) {
    	var check = false;
    	var re = /^\d{4}\-\d{1,2}\-\d{1,2}$/;
    	if( re.test(value)) {
    		var adata = value.split('-');
    		var year = parseInt(adata[0],10);
    		var month = parseInt(adata[1],10);
    		var day = parseInt(adata[2],10);
    		var xdata = new Date(year,month-1,day);
    		if ( ( xdata.getFullYear() === year ) && ( xdata.getMonth() === month - 1 ) && ( xdata.getDate() === day ) ){
    			check = true;
    		} else {
    			check = false;
    		}
    	} else {
    		check = false;
    	}
    	return check;
    }

    function validateTime(value) {
    	var check = false;
    	var adata = value.split(':');
    	var hours = parseInt(adata[0],10);
    	var minutes = parseInt(adata[1],10);
    	if((hours > 24) && (minutes > 60)) {
    		check=false;
    	} else {
    		check = true;
    	}
    	return check;
    }

	function dateOrder(value, element, options){
		var check = false;
		var start = $('#'+options.video_production_start_date).val();
		console.log("START DATE = " + start + ' END = ' + value);

		startDate = start.split('-');
		endDate = value.split('-');

		if(endDate[0]>=startDate[0] && endDate[1]>=startDate[1] && endDate[2]>=startDate[2]){
			check = true;
		}
		return check;
	}

	function startBeforeEnd(value, element, options){
		var check = false;
		var start = $('#'+options.start_time).val();
		var end = value;
		if(start < end){
			check = true;
		}
		else{
			check = false;
		}
		return check;
	}
    return {
        run: run
    };


});
