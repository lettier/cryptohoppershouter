#!/usr/bin/env python

'''

David Lettier (C) 2014.

Needs:

	- Python 2.7
	- Python-GNUPG http://code.google.com/p/python-gnupg/downloads/detail?name=python-gnupg-0.3.5.tar.gz
	
Usage:

	$python crypto_hopper.py OUT_FOLDER ENCRYPTED_FOLDER PUBLIC_KEY
	
Encrypts all files in OUT_FOLDER with the extension <.comp> and saves them to ENCRYPTED_FOLDER. 
Deletes all files in OUT_FOLDER that do not have the extension <.comp> and/or files that are older than 30 days.
	
'''

import sys;
import os;
import inspect;
import glob;
import time;
import errno;

gpg = None;

try:

	import gnupg;

	gpg = gnupg.GPG( );
	
except Exception:

	print "You need to install Python-GNUPG.";
	print "http://code.google.com/p/python-gnupg/";
	
	sys.exit( 1 );
	
# Gather command line parameters.
	
out_folder = None;

try:

	out_folder = sys.argv[ 1 ];
	
except Exception:

	print "No out folder specified.";
	
	sys.exit( 1 );
	
encrypted_folder = None;

try:

	encrypted_folder = sys.argv[ 2 ];
	
except Exception:

	print "No encrypted folder specified.";
	
	sys.exit( 1 );
	
public_key_file = None;

try:

	public_key_file = open( sys.argv[ 3 ], "r" );

	public_key_data = "";

	public_key_data_line = public_key_file.readline( );

	while public_key_data_line != "":

		public_key_data = public_key_data + public_key_data_line;
	
		public_key_data_line = public_key_file.readline( );
		
	imported_public_key = gpg.import_keys( public_key_data );
	
	public_key_file.close( );
		
except Exception as error:

	print "No public key specified.";
	
	print "Your public keys found:";
	
	public_keys = gpg.list_keys( );
	
	for public_key in public_keys:
	
		print "*****************";
		
		for key in public_key:
		
			print str( key ) + ":" + " " + str( public_key[ key ] );
			
	sys.exit( 1 );
	
# Gather files to encrypt and delete.
	
files_to_encrypt = [ ];
files_to_delete  = [ ];

if out_folder.endswith( "/" ):

	out_folder = out_folder[ : -1 ];
	
if encrypted_folder.endswith( "/" ):

	encrypted_folder = encrypted_folder[ : -1 ];

working_directory = os.getcwd( );

os.chdir( out_folder );

out_folder_lock_dir_file = out_folder + "/" + "dir.is.lck";

encrypted_folder_lock_dir_file = encrypted_folder + "/" + "dir.is.lck";

# Try to acquire a lock on the out folder.
# While no lock found, gather files to encrypt and delete.

exit = False;

for file in glob.glob( "*.*" ):

	if file == "dir.is.lck":
	
		exit = True;
		
		break;

	if file.endswith( ".comp" ):
	
		files_to_encrypt.append( os.path.abspath( file ) );
		
	elif not file.endswith( ".comp" ):
	
		days_old_since_last_modified = ( time.time( ) - os.path.getmtime( os.path.abspath( file ) ) ) / 86400.0;
		
		if days_old_since_last_modified >= 30.0:
		
			files_to_delete.append( os.path.abspath( os.path.abspath( file ) ) );
			
os.chdir( working_directory );
			
if exit:

	print "Out folder is locked. Try again later.";
	
	sys.exit( 0 );
	
else:

	# Set a lock on the out folder.
	
	f = open( out_folder_lock_dir_file, "w+" );
	
	f = f.close( );
	
os.chdir( encrypted_folder );

# Try to acquire a lock on the encrypted folder.

for file in glob.glob( "*.*" ):

	if file == "dir.is.lck":
	
		exit = True;
		
		break;
			
os.chdir( working_directory );
			
if exit:

	print "Encrypted folder is locked. Try again later.";
	
	sys.exit( 0 );
	
else:
	
	# Set a lock on the encrypted folder.
	
	f = open( encrypted_folder_lock_dir_file, "w+" );
	
	f = f.close( );
	
# Encrypt the files.
# Delete the >=30 day old files.
			
for file in files_to_encrypt:

	print "Encrypting: " + file;
	
	try:

		file_to_encrypt = open( file, "rb" );
	
		encrypted_file_data = gpg.encrypt_file( file_to_encrypt, imported_public_key.fingerprints, always_trust = True );
	
		file_to_encrypt.close( );
	
		file_path_of_file = os.path.dirname( os.path.realpath( file ) );
	
		encrypted_file = file.replace( file_path_of_file, "" );
	
		encrypted_file = open( encrypted_folder + encrypted_file, "w" );
	
		encrypted_file.write( str( encrypted_file_data ) );
	
		encrypted_file.close( );
		
		encrypted_file = file.replace( file_path_of_file, "" );
		
		encrypted_file_byte_size = os.path.getsize( encrypted_folder + encrypted_file );
		
		if encrypted_file_byte_size == 0:
		
			print "Could not encrypt file.";
			print "Encrypted file size is zero.";
			
			if os.path.isfile( out_lock_dir_file ):

				os.remove( out_folder_lock_dir_file );
				
			if os.path.isfile( encrypted_folder_lock_dir_file ):

				os.remove( encrypted_folder_lock_dir_file );
			
			break;
		
	except Exception, error:
	
		print "Could not encrypt file.";
		
		error_name = errno.errorcode[ error.errno ];
		
		if error_name == "ENOMEM":
		
			print "Out of memory.";
			
		elif error_name == "ENOSPC":
		
			print "No space left on device.";
			
		elif error_name == "ENOENT":
		
			print "No such file or directory.";
			
		else:
		
			print "Unknown error.";
			
		if os.path.isfile( out_folder_lock_dir_file ):

			os.remove( out_folder_lock_dir_file );
			
		if os.path.isfile( encrypted_folder_lock_dir_file ):

			os.remove( encrypted_folder_lock_dir_file );
		
		break;
		
	print "Success.";
	
for file in files_to_delete:
	
	print "Deleting file: " + file;

	if os.path.isfile( file ):

		os.remove( file );
		
		print "Success."
	
	else:

		print "Could not delete file.";
	
		continue;
		
# Remove locks.
		
if os.path.isfile( out_folder_lock_dir_file ):

	os.remove( out_folder_lock_dir_file );
	
if os.path.isfile( encrypted_folder_lock_dir_file ):

	os.remove( encrypted_folder_lock_dir_file );

