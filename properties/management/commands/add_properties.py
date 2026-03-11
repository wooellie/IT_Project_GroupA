from django.core.management.base import BaseCommand
from django.core.files import File
from properties.models import Property, User
from pathlib import Path


class Command(BaseCommand):
    help = 'Add Glasgow student properties'

    def handle(self, *args, **kwargs):
        owner = User.objects.filter(role='agency').first()
        if not owner:
            self.stdout.write(self.style.ERROR('No agency user found'))
            return

        properties_data = [
            {
                'title': 'George Street Apartments',
                'address': '151 George Street, Glasgow G1 1AB',
                'zip_code': 'G1 1AB',
                'price': 226,
                'distance': '2.4mi',
                'latitude': 55.8607327,
                'longitude': -4.2545769,
                'image': 'room1.jpg',
                'description': 'Modern studio apartment in the heart of Glasgow city centre. Features contemporary furnishings, en-suite bathroom, and fully equipped kitchen. Perfect for students seeking city living with excellent transport links to campus.'
            },
            {
                'title': 'Merchant Studios',
                'address': '6 Havannah Street, Glasgow, G4 0AJ, United Kingdom',
                'zip_code': 'G4 0AJ',
                'price': 199,
                'distance': '2.8mi',
                'latitude': 55.8597247,
                'longitude': -4.2478641,
                'image': 'room2.jpg',
                'description': 'Stylish student studio in vibrant Merchant City. Spacious living area with dedicated study space, modern kitchen facilities, and superfast WiFi. Close to shops, restaurants, and nightlife.'
            },
            {
                'title': 'Gibson Street Apartments',
                'address': 'Gibson Street, Glasgow G12 8SY, United Kingdom',
                'zip_code': 'G12 8SY',
                'price': 199,
                'distance': '0.2mi',
                'latitude': 55.8730289,
                'longitude': -4.2874552,
                'image': 'room3.jpg',
                'description': 'Prime West End location just minutes from campus. Bright and airy studio with modern amenities, private bathroom, and study desk. Surrounded by cafes, bars, and the beautiful Kelvingrove Park.'
            },
            {
                'title': 'Dunaskin Mill',
                'address': 'Dunaskin Mill 5 Dunaskin Court Glasgow G11 6QJ',
                'zip_code': 'G11 6QJ',
                'price': 215,
                'distance': '0.2mi',
                'latitude': 55.869251,
                'longitude': -4.3000607,
                'image': 'room4.jpg',
                'description': 'Contemporary student accommodation in trendy Partick. Features open-plan living with modern kitchen, comfortable sleeping area, and excellent storage. Walking distance to Partick Station and campus.'
            },
            {
                'title': 'Vita Student West End, Glasgow',
                'address': '21 Beith Street, Glasgow, G11 6BZ',
                'zip_code': 'G11 6BZ',
                'price': 215,
                'distance': '0.5mi',
                'latitude': 55.8689455,
                'longitude': -4.308302,
                'image': 'room5.jpg',
                'description': 'Premium student living with fantastic communal facilities including gym, cinema room, and study spaces. Modern studio with stylish decor, fully-fitted kitchen, and en-suite bathroom. Perfect student community atmosphere.'
            },
            {
                'title': 'West Village',
                'address': 'Beith Street, Glasgow G11 6PS',
                'zip_code': 'G11 6PS',
                'price': 159,
                'distance': '0.4mi',
                'latitude': 55.8692558,
                'longitude': -4.3111955,
                'image': 'room6.jpg',
                'description': 'Affordable student accommodation in the West End. Comfortable studio with all essentials including study area, kitchenette, and private bathroom. Great value in excellent location close to campus and local amenities.'
            },
            {
                'title': 'Canvas Glasgow',
                'address': 'Boyce House, 47 Kyle Street, Glasgow, G4 0JQ',
                'zip_code': 'G4 0JQ',
                'price': 161,
                'distance': '1.9mi',
                'latitude': 55.8679751,
                'longitude': -4.24932,
                'image': 'room7.jpg',
                'description': 'Modern purpose-built student residence with excellent facilities. Studio features contemporary design, fully-equipped kitchen, and comfortable living space. On-site laundry, bike storage, and 24/7 security.'
            },
            {
                'title': 'St Mungo\'s',
                'address': '200 St James Rd, Glasgow G4 0NT, United Kingdom',
                'zip_code': 'G4 0NT',
                'price': 185,
                'distance': '2mi',
                'latitude': 55.8647257,
                'longitude': -4.2456359,
                'image': 'room8.jpg',
                'description': 'Quality student accommodation in North Glasgow. Well-designed studio with modern furnishings, private bathroom, and compact kitchen. Good transport connections to campus and city centre. Quiet residential area ideal for studying.'
            }
        ]

        base_path = Path(__file__).resolve().parent.parent.parent.parent
        media_path = base_path / 'media' / 'images'
        
        count = 0
        for data in properties_data:
            if Property.objects.filter(title=data['title']).exists():
                continue

            prop = Property(
                title=data['title'],
                address=data['address'],
                zip_code=data['zip_code'],
                price=data['price'],
                distance_from_campus=data['distance'],
                latitude=data['latitude'],
                longitude=data['longitude'],
                description=data['description'],
                owner=owner
            )

            img_path = media_path / data['image']
            if img_path.exists():
                with open(img_path, 'rb') as f:
                    prop.image.save(data['image'], File(f), save=False)

            prop.save()
            count += 1

        self.stdout.write(f'Created {count} properties')