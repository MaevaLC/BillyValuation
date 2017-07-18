# Dimitri Masson (dhmmasson)
# This module get the access token from google
# USAGE: 
# getToken( 'ideavaluation-fa9d97a5c0f0.json' )
import requests   
import json
import jwt
import os #To  get environement variable 
import datetime

#get the token for the service account identified by the credentials in credentialsFile
def getToken( CredentialFilename, scopes=None ): 
	serviceInfo= __getServiceInfo( CredentialFilename )
	privateKey = serviceInfo.get( 'private_key' )
	email = serviceInfo.get( 'client_email' )
	if( scopes is None ):
		scopes = 'https://www.googleapis.com/auth/cloud-platform'
	assertionToken = __createAssertionToken( email, privateKey, scopes )
	accessToken = __getAccessToken( assertionToken )
	return accessToken.get( 'access_token' )


# get the info directly from the google credential file
def __getServiceInfo( filename ):
	credentialsFile = open( filename, 'r' )
	credentials = json.load( credentialsFile )
	return credentials 


#TODO: Obsolete should be remove
def __getPrivateKey( filename='privateKey' ):
	#if the key is in the environement use this one
	key = os.environ.get( 'GOOGLE_PRIVATE_KEY' )
	if( key == None ):
		keyFile = open( filename, 'r' )
		key = keyFile.read() 
	return key 

#This function create a token that identify our service to ask for an access token 
#@param email the email of the service account
#@param privateKey 
def __createAssertionToken( email, privateKey=None, scopes=None ):
	#get the privateKey if none is provided
	if( privateKey is None ):
		privateKey = __getPrivateKey 
	if( scopes is None ):
		scopes='https://www.googleapis.com/auth/cloud-platform'
	demands= { 'iss'	: email, 
			   'scope'	: scopes,
			   'aud'	: 'https://www.googleapis.com/oauth2/v4/token',
			   'exp'	: datetime.datetime.utcnow() + datetime.timedelta(hours=1), 
			   'iat'	: datetime.datetime.utcnow() 
			}
	assertionToken = jwt.encode( demands, privateKey, algorithm='RS256' )

	return assertionToken

#get the accessToken from google 
def __getAccessToken( assertionToken ): 
	accessToken = requests.post( 'https://www.googleapis.com/oauth2/v4/token'
							   , data = { 'grant_type' : 'urn:ietf:params:oauth:grant-type:jwt-bearer',
							   			  'assertion'  : assertionToken
							   			}
							   	).json() 
	return accessToken

