from __future__ import absolute_import

from django.core.urlresolvers import reverse

from sentry.models import File, Release, ReleaseFile
from sentry.testutils import APITestCase


class ReleaseDetailsTest(APITestCase):
    def test_simple(self):
        self.login_as(user=self.user)

        project = self.create_project(name='foo')
        release = Release.objects.create(
            project=project,
            version='1',
        )

        url = reverse('sentry-api-0-release-details', kwargs={
            'project_id': project.id,
            'version': release.version,
        })
        response = self.client.get(url)

        assert response.status_code == 200, response.content
        assert response.data['version'] == release.version


class ReleaseDeleteTest(APITestCase):
    def test_simple(self):
        self.login_as(user=self.user)

        project = self.create_project(name='foo')
        release = Release.objects.create(
            project=project,
            version='1',
        )
        releasefile = ReleaseFile.objects.create(
            project=project,
            release=release,
            file=File.objects.create(
                path='http://example.com',
                name='application.js',
                type='release.file',
            ),
            name='http://example.com/application.js'
        )

        url = reverse('sentry-api-0-release-details', kwargs={
            'project_id': project.id,
            'version': release.version,
        })
        response = self.client.delete(url)

        assert response.status_code == 204, response.content

        assert not Release.objects.filter(id=release.id).exists()
