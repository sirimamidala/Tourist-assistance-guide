# Hill Stations Feature - Setup & Usage Guide

## 🎯 Overview

The Hill Stations feature has been successfully implemented in the Tourist Assistance Guide Django project. This feature allows users to explore and discover beautiful hill stations across India with detailed information, location maps, and admin management capabilities.

## ✅ What's Included

### 1. **Database Model (HillStation)**
- **Location**: `explorer/models.py`
- **Fields**:
  - Name
  - City
  - District
  - State
  - Country
  - Description
  - Best Time to Visit
  - Temperature Range
  - Latitude (for map integration)
  - Longitude (for map integration)
  - Image (uploaded to `media/explorer/hill_stations/`)
  - Created Date

### 2. **Admin Features**
- **Location**: `explorer/admin.py`
- Admin-only access to add, edit, and delete hill stations
- List view with filters by state and country
- Search functionality by name, city, district, and state
- Fieldsets for organized form display

### 3. **Forms**
- **Location**: `explorer/forms.py`
- `HillStationForm`: Bootstrap-styled form for adding/editing hill stations
- Input validation for all fields
- Custom styling with form controls

### 4. **Views**
- **Location**: `explorer/views.py`
- `hill_stations_list()`: Public list view with search and filter
- `hill_station_detail()`: Detailed view with Google Map integration
- `hill_station_add()`: Admin-only view to add new hill stations
- `hill_station_edit()`: Admin-only view to edit existing hill stations
- `hill_station_delete()`: Admin-only view to delete hill stations

### 5. **URLs**
- **Location**: `explorer/urls.py`
- `/explorer/hill-stations/` - List view
- `/explorer/hill-stations/<id>/` - Detail view
- `/explorer/hill-stations/add/` - Add new hill station (Admin only)
- `/explorer/hill-stations/<id>/edit/` - Edit hill station (Admin only)
- `/explorer/hill-stations/<id>/delete/` - Delete hill station (Admin only)

### 6. **Templates**
- **Location**: `templates/explorer/`
- `hill_stations_list.html`: Card-based list with responsive grid layout
- `hill_station_detail.html`: Detailed view with Google Map
- `hill_station_form.html`: Bootstrap-styled form
- `hill_station_confirm_delete.html`: Confirmation page

### 7. **Features Implemented**
✅ Search by State
✅ Filter by City
✅ Google Maps Integration (ready for API key)
✅ Image Upload & Storage
✅ Bootstrap Responsive UI
✅ Admin-Only Management
✅ Public View Access
✅ Seed Data Script (10 popular hill stations)

## 🚀 Getting Started

### Step 1: Database Setup
The migration has already been applied:
```bash
python manage.py makemigrations explorer  # (Already done)
python manage.py migrate explorer  # (Already done)
```

### Step 2: Load Sample Data
```bash
python seed_hill_stations.py
```
This will create 10 sample hill stations with placeholder images.

### Step 3: Start the Server
```bash
python manage.py runserver
```

### Step 4: Access the Features

**Public Views:**
- List: `http://localhost:8000/explorer/hill-stations/`
- Detail: `http://localhost:8000/explorer/hill-stations/1/`

**Admin Panel:**
- Admin: `http://localhost:8000/admin/`
- Add Hill Station: `http://localhost:8000/explorer/hill-stations/add/`
- Edit: `http://localhost:8000/explorer/hill-stations/<id>/edit/`
- Delete: `http://localhost:8000/explorer/hill-stations/<id>/delete/`

## 🗺️ Google Maps Integration

To enable Google Maps on the detail page:

1. **Get API Key**:
   - Visit [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project
   - Enable Maps JavaScript API
   - Create an API key

2. **Update Template**:
   - Open `templates/explorer/hill_station_detail.html`
   - Replace `YOUR_GOOGLE_MAPS_API_KEY` with your actual API key:
   ```html
   <script src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&libraries=places"></script>
   ```

## 🎨 Styling & UI

All templates use:
- **Bootstrap 5** for responsive grid layout
- **Custom CSS** with glassmorphism design
- **Hover effects** for better UX
- **Card-based layout** for hill stations
- **Color scheme**: Dark theme with accent colors

## 📊 Admin Management

### Adding a Hill Station:
1. Go to Admin Panel → Hill Stations
2. Click "Add Hill Station"
3. Fill in all required fields
4. Upload a high-quality image
5. Enter latitude/longitude for map
6. Save

### Searching & Filtering:
- Search by: Name, City, District, State
- Filter by: State, Country
- Quick access to edit/delete actions

## 🔐 Access Control

- **Public Users**: Can view list and details
- **Staff/Admin Users**: Can add, edit, and delete
- Decorators: `@staff_member_required` on all admin views

## 📁 File Structure

```
explorer/
├── models.py          # HillStation model
├── admin.py           # Admin configuration
├── forms.py           # HillStationForm
├── views.py           # All views
├── urls.py            # URL patterns
└── migrations/
    └── 0002_hillstation_alter_place_category.py

templates/explorer/
├── hill_stations_list.html         # List with search/filter
├── hill_station_detail.html        # Detail with map
├── hill_station_form.html          # Add/Edit form
└── hill_station_confirm_delete.html # Delete confirmation

seed_hill_stations.py               # Sample data script
```

## 🔍 Search Features

### In List View:
- **Search by State**: Filter hill stations by Indian states
- **Search by City**: Filter by specific cities
- **Clear Button**: Reset all filters

### Responsive Layout:
- Desktop: 3 columns per row
- Tablet: 2 columns per row
- Mobile: 1 column per row

## 🖼️ Media Management

- Images stored at: `media/explorer/hill_stations/`
- MEDIA_URL: `/media/`
- MEDIA_ROOT: Configured in settings.py
- Supported formats: JPG, PNG, GIF

## 📝 Sample Data

10 popular hill stations included:
1. Shimla - Himachal Pradesh
2. Manali - Himachal Pradesh
3. Darjeeling - West Bengal
4. Ooty - Tamil Nadu
5. Munnar - Kerala
6. Nainital - Uttarakhand
7. Mussoorie - Uttarakhand
8. Coorg - Karnataka
9. Coonoor - Tamil Nadu
10. Kasauli - Himachal Pradesh

## 🎯 Customization Tips

### Adding More Hill Stations:
Edit `seed_hill_stations.py` and add to the `hill_stations_data` list:
```python
{
    "name": "Your Hill Station",
    "city": "City Name",
    "district": "District Name",
    "state": "State Name",
    "country": "India",
    "description": "Your description...",
    "best_time_to_visit": "Month1-Month2",
    "temperature_range": "XoC - YoC",
    "latitude": XX.XXXX,
    "longitude": XX.XXXX,
    "image_url": "https://..."
}
```

### Modifying Styling:
- CSS is embedded in templates
- Modify color variables in base.html
- Update Bootstrap classes as needed

## ⚙️ Configuration

### Settings.py (Already Configured)
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

### urls.py (Main project)
Make sure to include media files in development:
```python
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

## 🐛 Troubleshooting

**Images not displaying?**
- Check MEDIA_URL and MEDIA_ROOT in settings.py
- Ensure media files are uploaded to correct folder
- Add media URL to main urls.py

**Map not showing?**
- Verify Google Maps API key is correct
- Check browser console for errors
- Ensure coordinates (latitude/longitude) are valid

**Admin actions not visible?**
- Check if user is staff member
- Verify @staff_member_required decorator is in place

## 🎓 Next Steps

1. Add more hill stations via admin panel
2. Customize images for each location
3. Enable Google Maps with your API key
4. Add weather integration
5. Implement user reviews/ratings
6. Add multilingual support
7. Create API endpoints using DRF

## 📞 Support

For issues or questions, check:
- Django admin panel for data management
- Console errors for debugging
- Template files for styling adjustments

---

**Feature implemented successfully! 🎉 Enjoy exploring hill stations!**
