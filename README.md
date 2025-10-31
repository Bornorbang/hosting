# HostingPro - Django + Tailwind CSS Website

A modern, responsive website for a domain and hosting company built with Django and Tailwind CSS.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm

### Setup Instructions

1. **Install Python Dependencies**
   ```bash
   pip install django
   ```

2. **Install Node.js Dependencies**
   ```bash
   npm install
   ```

3. **Build CSS (Production)**
   ```bash
   npm run build-css-prod
   ```

4. **Run Django Development Server**
   ```bash
   python manage.py runserver
   ```

5. **For Development with Auto-rebuilding CSS**
   
   Open two terminals:
   
   Terminal 1 (CSS watching):
   ```bash
   npm run dev
   # or on Windows: start-tailwind.bat
   ```
   
   Terminal 2 (Django server):
   ```bash
   python manage.py runserver
   ```

## 📁 Project Structure

```
hosting/
├── app/                    # Main Django app
├── hosting/               # Django project settings
├── templates/             # HTML templates
│   ├── base.html         # Base template with navigation/footer
│   └── home.html         # Homepage template
├── static/               # Static files
│   ├── css/
│   │   ├── input.css     # Tailwind input file
│   │   └── output.css    # Generated CSS (don't edit)
│   ├── js/               # JavaScript files
│   └── images/           # Image assets
├── tailwind.config.js    # Tailwind configuration
├── package.json          # Node.js dependencies
└── manage.py            # Django management script
```

## 🎨 Tailwind CSS Usage

### Custom Components
Pre-built components are available in `static/css/input.css`:

- `.btn-primary` - Primary blue button
- `.btn-secondary` - Secondary gray button  
- `.card` - White card with shadow
- `.hero-gradient` - Blue gradient background
- `.animate-fadeInUp` - Fade in up animation

### Color Palette
Custom colors defined in `tailwind.config.js`:

- `primary-*` - Blue color scale (50-900)
- `hosting-dark` - Dark theme color
- `hosting-light` - Light theme color
- `hosting-accent` - Orange accent color

### Development Workflow

1. **Adding New Styles:**
   - Use Tailwind utility classes in templates
   - Add custom components to `static/css/input.css` if needed
   - Rebuild CSS: `npm run build-css-prod`

2. **Making Template Changes:**
   - Edit templates in `templates/` folder
   - Use existing components or Tailwind utilities
   - Run `npm run dev` for auto-rebuilding during development

3. **Adding New Pages:**
   - Create template in `templates/`
   - Add view in `app/views.py`
   - Add URL pattern in `hosting/urls.py`

## 🛠️ Available NPM Scripts

- `npm run dev` - Watch for changes and rebuild CSS automatically
- `npm run build-css` - Build CSS with watch mode
- `npm run build-css-prod` - Build minified CSS for production

## 📱 Features

### Current Features
- ✅ Responsive design (mobile-first)
- ✅ Modern navigation with mobile menu
- ✅ Hero section with call-to-action
- ✅ Feature highlights
- ✅ Pricing plans section
- ✅ Professional footer
- ✅ Custom animations
- ✅ SEO-friendly structure

### Ready for Extension
- 🔧 Contact forms
- 🔧 Domain search functionality
- 🔧 Customer portal
- 🔧 Blog/news section
- 🔧 Support ticket system

## 🎯 Customization

### Branding
Update these elements to match your brand:

1. **Company Name:** Change "HostingPro" in `templates/base.html`
2. **Colors:** Modify color palette in `tailwind.config.js`
3. **Logo:** Add logo image to `static/images/` and update navigation
4. **Content:** Update homepage content in `templates/home.html`

### Fonts
Currently using Google Fonts (Inter + Poppins). To change:

1. Update font links in `templates/base.html`
2. Modify font family in `tailwind.config.js`

## 🚀 Deployment

### Production CSS Build
```bash
npm run build-css-prod
```

### Static Files Collection
```bash
python manage.py collectstatic
```

### Environment Variables
Set these in production:
- `DEBUG=False`
- `SECRET_KEY=your-secret-key`
- `ALLOWED_HOSTS=your-domain.com`

## 📝 Notes

- The CSS output file (`static/css/output.css`) is generated automatically - don't edit it directly
- Always use `npm run build-css-prod` before deploying to production
- The project uses Django's static files handling for CSS/JS/images
- Mobile-first responsive design approach
- Optimized for performance and SEO

## 🤝 Contributing

1. Make changes to templates or input CSS
2. Test locally with `npm run dev` + `python manage.py runserver`
3. Build production CSS with `npm run build-css-prod`
4. Commit all changes including the generated CSS file