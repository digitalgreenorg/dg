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
function check_validation(file,email_id,block)
			{
				email_confirm = "Send an email with error files to " +email_id.value+ " ?"; 
				if(email_valid == 1)
				{
					if(email_id.value.length < 1)
					{
						alert("Enter email id OR uncheck the email box");
						event.preventDefault();
					}
					else
					{
						alert(email_confirm);
					}
				}
				if(block.value=="-- select an option --")
				{
					alert("Block should be selected before proceeding");
					event.preventDefault();
				}
				var ext = [ "xls", "xlsx", "csv"]
				var file_part = file.value.split('.');
				var extension = file_part[1];
				var flag=0;
				
				if (file.value == "")
				{
					alert("Select a file to be uploaded");
					event.preventDefault();
				}
				
				for ( var i=0; i< ext.length; i++)
				{
					
						
					if (extension.localeCompare(ext[i])==0)
				 	{
				 		flag=1;
				 		break;
					}
				}
				if(flag==0)
				{
					alert("Invalid file format");
					event.preventDefault();
					
				}
				alert("File is being uploaded, this may take few minutes. Please do not refresh or send another upload request. you will be automatically redirected to another page")

				
			}
