from django.test import TestCase, override_settings
from django.urls import reverse
from django.db import IntegrityError

from .models import User, Property, Like, Collection, Review, AgencyProfile


@override_settings(GOOGLE_MAPS_API_KEY="test-key")
class ModelTest(TestCase):
    def setUp(self):
        self.student = User.objects.create_user(
            username="unitstudent",
            password="test123",
            role="user"
        )
        self.agency = User.objects.create_user(
            username="unitagency",
            password="test123",
            role="agency"
        )

        self.property = Property.objects.create(
            title="Test Flat",
            description="Test Flat",
            price=777,
            zip_code="G4 0PS",
            address="St James Road 110",
            area="West End",
            user=self.agency
        )

    def test1(self):
        self.assertEqual(self.property.user, self.agency)

    def test2(self):
        Like.objects.create(user=self.student, property=self.property)
        with self.assertRaises(IntegrityError):
            Like.objects.create(user=self.student, property=self.property)

    def test3(self):
        collection = Collection.objects.create(user=self.student, property=self.property)
        self.assertEqual(collection.user, self.student)
        self.assertEqual(collection.property, self.property)

    def test4(self):
        profile = AgencyProfile.objects.create(user=self.agency, agency_name="unitagency")

        Review.objects.create(
            user=self.student,
            property=self.property,
            rating=4,
            comment="I love this place"
        )

        student2 = User.objects.create_user(
            username="unitstudent1",
            password="testp123",
            role="user"
        )

        property2 = Property.objects.create(
            title="Test Flat 2",
            description="Test Flat 2",
            price=776,
            zip_code="G4 0PA",
            address="456 Test Road",
            area="Cowcaddens",
            user=self.agency
        )

        Review.objects.create(
            user=student2,
            property=property2,
            rating=2,
            comment="Bad, did not like it"
        )

        self.assertEqual(profile.get_avg_rating(), 3.0)


class ViewTest(TestCase):
    def setUp(self):
        self.student = User.objects.create_user(
            username="unitstudent",
            password="test123",
            role="user"
        )
        self.agency = User.objects.create_user(
            username="unitagency",
            password="test123",
            role="agency"
        )

        self.property = Property.objects.create(
            title="Test Flat",
            description="Test Flat",
            price=777,
            zip_code="G4 0PS",
            address="St James Road 110",
            area="West End",
            user=self.agency
        )

    def test1(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test2(self):
        response = self.client.get(reverse("property_detail", args=[self.property.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)

    def test3(self):
        self.client.login(username="unitagency", password="test123")
        response = self.client.post(reverse("post_property"), {
            "title": "Test Flat 3",
            "description": "Test Flat 3",
            "price": 333,
            "zip_code": "G4 0PB",
            "address": "St James Road 111",
            "area": "Cowcaddens"
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Property.objects.filter(title="Test Flat 3", user=self.agency).exists())

    def test4(self):
        self.client.login(username="unitstudent", password="test123")
        response = self.client.post(reverse("property_detail", args=[self.property.pk]), {
            "rating": 5,
            "comment": "Amazing Property!"
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Review.objects.filter(user=self.student, property=self.property).exists())