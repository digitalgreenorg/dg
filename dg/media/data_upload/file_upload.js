        		
// function to check extension of uploading file
function check_validation(file,email_id,block)
			{
				email_confirm = "Send an email with error files to " +email_id.value+ " ?"; 
				var ext = [ "xls", "xlsx", "csv"]
				var file_part = file.value.split('.');
				var extension = file_part[1];
				var flag=0;
				
				if(block.value!="-- select an option --")
				{
					if(email_id.value.length > 1)
					{
						var confirm = window.confirm(email_confirm);
						
						if (file.value != "")
						{
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
							else
							{
								if (confirm == false)
								{
									alert("Enter valid email id");
									event.preventDefault();
								}	
								else
								{
									alert("File is being uploaded, it will take FEW MINUTES. Please don't refresh or click on upload button. You will be directly redirected to another page.");
						    	}
							}
						}
						else
						{	alert("Select a file to be uploaded");
							event.preventDefault();
						}
					}
					else
					{
						alert("Enter email id");
						event.preventDefault();	
					}
				}	
				else{
						alert("Block should be selected before proceeding");
						event.preventDefault();
					}
	}

	

		