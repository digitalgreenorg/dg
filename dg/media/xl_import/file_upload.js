var email_valid = 0;
// function to show and hide message box 
function showHide() { 
        				
            			if (document.getElementById('email_box').checked) {
            				
							 email_valid = 1;
                			document.getElementById('get_email').style.visibility = 'visible'; 
            				} 
            			else {
            				
                			document.getElementById('get_email').style.visibility = 'hidden'; 
            				} 
            		}
            		
// function to check extension of uploading file
function check_extension(file,email_id)
			{
				if(email_valid == 1)
				{
					if(email_id.value.length < 1)
					{
						alert("Enter email id");
					}
					else
					{
						alert(email_id.value);
					}
				}
				var ext = [ "xls", "xlsx", "csv"]
				var file_part = file.value.split('.');
				var extension = file_part[1];
				var flag=0;
				
				for ( var i=0; i< ext.length; i++)
				{
					
						
					if (extension.localeCompare(ext[i])==0)
				 	{
				 		flag=1;
				 		//function function();
				 		break;
					}
				}
				if(flag==0)
				{
					alert("Invalid file format");
				}
			}
