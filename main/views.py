from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import google_auth_oauthlib.flow
from django.shortcuts import redirect
import requests

CLIENT_SECRET = {
    "web":{
        "client_id":"1075849008798-69tg99se9q9ngm2a3g91u8cjkkj0oo5c.apps.googleusercontent.com",
        "project_id":"convinassignment-347521",
        "auth_uri":"https://accounts.google.com/o/oauth2/auth",
        "token_uri":"https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs",
        "client_secret":"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",
        "redirect_uris":["http://localhost:8000/"]
    }
}

SCOPES = ['https://www.googleapis.com/auth/calendar.events.readonly']


class GoogleCalendarInitView(APIView):
    def get(self, request):
        flow = google_auth_oauthlib.flow.Flow.from_client_config(
            CLIENT_SECRET,
            scopes=SCOPES)
        flow.redirect_uri = 'http://localhost:8000/rest/v1/calendar/redirect'

        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true')

        return redirect(authorization_url)


class GoogleCalendarRedirectView(APIView):
    def get(self, request):
        state = request.GET.get('state', '')
        flow = google_auth_oauthlib.flow.Flow.from_client_config(
            CLIENT_SECRET,
            scopes=SCOPES,
            state=state)
        flow.redirect_uri = 'http://localhost:8000/rest/v1/calendar/redirect'

        authorization_response = request.build_absolute_uri().replace('http', 'https')
        flow.fetch_token(authorization_response=authorization_response)

        credentials = flow.credentials
        r = requests.get(
            'https://www.googleapis.com/calendar/v3/calendars/primary/events',
            headers={
                'Authorization': 'Bearer '+ credentials.token
            })
        return Response(r.json()['items'], status=status.HTTP_200_OK)
