#!/usr/bin/env python

'''

David Lettier (C) 2014.

Needs:

	- Python 2.7
	
Usage:

	$python crypto_shouter.py ENCRYPTED_FOLDER TRASH_FOLDER EMAIL_USERNAME@EMAIL_PROVIDER.EXT EMAIL_PASSWORD SMTP_SERVER:PORT_NUMBER EMAIL_ADDRESS1 EMAIL_ADDRESS2 ... EMAIL_ADDRESSn 
	
Emails all encrypted files in ENCRYPTED_FOLDER to EMAIL_ADDRESS1 EMAIL_ADDRESS2 ... EMAIL_ADDRESSn.
Moves these encrypted files, emailed, to TRASH_FOLDER.
Deletes all encrypted files in TRASH_FOLDER that are older than 30 days.
	
'''

import smtplib, os, sys, glob, time;
from email.MIMEMultipart import MIMEMultipart;
from email.MIMEBase import MIMEBase;
from email.MIMEText import MIMEText;
from email.Utils import COMMASPACE, formatdate;
from email import Encoders;

# Most of the following function was taken from: http://stackoverflow.com/questions/3362600/how-to-send-email-attachments-with-python

def send_mail( login, password, send_from, send_to, subject, text, files, server_and_port_number ):

	assert type( send_to ) == list;

	assert type( files ) == list;

	msg = MIMEMultipart( );
	msg[ 'From' ]    = send_from;
	msg[ 'To' ]      = COMMASPACE.join( send_to );
	msg[ 'Date' ]    = formatdate( localtime = True );
	msg[ 'Subject' ] = subject;

	msg.attach( MIMEText( text ) );

	for f in files:

		part = MIMEBase( 'application', "octet-stream" );
		part.set_payload( open( f,"rb" ).read( ) );
		Encoders.encode_base64( part );
		part.add_header( 'Content-Disposition', 'attachment; filename="%s"' % os.path.basename( f ) );
		msg.attach( part );

	smtp = smtplib.SMTP( server_and_port_number );
	smtp.starttls( );
	smtp.login( login, password );
	result = smtp.sendmail( send_from, send_to, msg.as_string( ) );
	smtp.close( );
	
	return result;
	
# Gather parameters.
	
encrypted_folder = None;

try:

	encrypted_folder = sys.argv[ 1 ];
	
except Exception:

	print "No encrypted folder specified.";
	
	sys.exit( 1 );
	
trash_folder = None;

try:

	trash_folder = sys.argv[ 2 ];
	
except Exception:

	print "No trash folder specified.";
	
	sys.exit( 1 );
	
email_one = None;

email_user_name = None;

try:

	email_user_name = sys.argv[ 3 ];
	
except Exception:

	print "No email username specified.";
	
	sys.exit( 1 );
	
email_password = None;

try:

	email_password = sys.argv[ 4 ];
	
except Exception:

	print "No email password specified.";
	
	sys.exit( 1 );
	
smtp_server_and_port_number = None;

try:

	smtp_server_and_port_number = sys.argv[ 5 ];
	
except Exception:

	print "No SMTP server and port number specified.";
	
	sys.exit( 1 );
	
email_one = None;

try:

	email_one = sys.argv[ 6 ];
	
except Exception:

	print "No email(s) specified.";
	
	sys.exit( 1 );
	
send_to_emails = [ email_one ];

try:

	i = 7;

	while True:

		send_to_emails.append( sys.argv[ i ] );
	
		i = i + 1;
		
except Exception:

	pass
	
encrypted_files_to_send    = [ ];

if encrypted_folder.endswith( "/" ):

	encrypted_folder = encrypted_folder[ : -1 ];

if trash_folder.endswith( "/" ):

	trash_folder = trash_folder[ : -1 ];

working_directory = os.getcwd( );

os.chdir( encrypted_folder );

encrypted_folder_lock_dir_file = encrypted_folder + "/" + "dir.is.lck";

# Try to acquire a lock on the encrypted folder.
# While no lock found, gather the encrypted files to email.

exit = False;

for file in glob.glob( "*.*" ):

	if file == "dir.is.lck":
	
		exit = True;
		
		break;

	if file.endswith( ".comp" ):
	
		encrypted_files_to_send.append( os.path.abspath( file ) );
			
os.chdir( working_directory );

if exit:

	print "Encrypted folder is locked. Try again later.";
	
	sys.exit( 0 );
	
else:
	
	# Set a lock on the encrypted folder.
	
	f = open( encrypted_folder_lock_dir_file, "w+" );
	
	f = f.close( );
	
# Email the files.

if len( encrypted_files_to_send ) != 0:
	
	email_subject = "[ CryptoShouter ] Encrypted files enclosed.";
	email_message = "Hello from CryptoShouter. Attached are your encrypted files.";
	
	print "Emailing encrypted files."
	
	result = send_mail( email_user_name, email_password, email_user_name, send_to_emails, email_subject, email_message, encrypted_files_to_send, smtp_server_and_port_number );
	
	if len( result ) != 0:
	
		print "Error emailing encrypted files."
		
		# Remove lock.
		
		if os.path.isfile( encrypted_folder_lock_dir_file ):

			os.remove( encrypted_folder_lock_dir_file );
		
		sys.exit( 0 );
		
	else:
	
		print "Success.";
		
	# Move the files.
	
	for file in encrypted_files_to_send:
	
		print "Moving file to trash folder: " + file
		
		file_path_of_file = os.path.dirname( os.path.realpath( file ) );
	
		encrypted_file = file.replace( file_path_of_file, "" );
		
		try:
		
			os.rename( file, trash_folder + "/" + encrypted_file );
			
			print "Success."
			
		except Exception:
		
			print "Could not move file."
			
			continue;
			
else:

	print "No encrypted files found.";
	
# Empty out the trash for files >=30 days old.
	
os.chdir( trash_folder );

for file in glob.glob( "*.*" ):
	
	days_old_since_last_modified = ( time.time( ) - os.path.getmtime( os.path.abspath( file ) ) ) / 86400.0;
	
	if days_old_since_last_modified >= 30.0:
	
		print "Deleting file: " + file;

		if os.path.isfile( file ):

			os.remove( file );
			
			print "Success.";
	
		else:

			print "Could not delete file.";
	
			continue;
			
# Remove lock.
			
os.chdir( working_directory );
			
if os.path.isfile( encrypted_folder_lock_dir_file ):

	os.remove( encrypted_folder_lock_dir_file );

