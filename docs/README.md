# VSD Fleet Management System Documentation

This directory contains the comprehensive documentation for the VSD Fleet Management System, built using [MkDocs](https://www.mkdocs.org/) with the [Material theme](https://squidfunk.github.io/mkdocs-material/).

## 📚 Documentation Structure

```
docs/
├── index.md                    # Main landing page
├── installation.md             # Installation guide
├── how-to-use.md              # Basic usage guide
├── faq.md                     # Frequently asked questions
├── changelog.md               # Version history
├── user-guide/                # User guides
│   └── complete-workflow.md   # End-to-end workflow guide
├── transactions/              # Transaction documentation
│   ├── cargo-registration.md  # Cargo registration guide
│   ├── manifest-management.md # Manifest management guide
│   ├── trip-management.md     # Trip management guide
│   └── financial-workflows.md # Financial workflows guide
├── api/                       # API documentation
│   └── doctype-reference.md   # Complete doctype reference
├── setup/                     # Setup guides
│   ├── master.md             # Master data setup
│   └── configuration.md      # Configuration guide
├── features/                  # Feature documentation
│   ├── gps-tracking.md       # GPS tracking features
│   └── maintenance.md        # Maintenance features
└── assets/                    # Images and static files
    ├── truck.svg             # Logo and icons
    └── workspace.png         # Screenshots
```

## 🚀 Getting Started

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Installation
1. Install MkDocs and the Material theme:
   ```bash
   pip install mkdocs mkdocs-material
   ```

2. Navigate to the project root:
   ```bash
   cd /path/to/vsd_fleet_ms
   ```

3. Serve the documentation locally:
   ```bash
   mkdocs serve
   ```

4. Open your browser and go to `http://127.0.0.1:8000`

### Building for Production
To build the documentation for production deployment:
```bash
mkdocs build
```

This creates a `site/` directory with the static HTML files.

## 📖 Documentation Sections

### 1. **Complete Workflow Guide** (`user-guide/complete-workflow.md`)
- **Purpose**: End-to-end process documentation
- **Audience**: New users, implementation teams
- **Content**: Complete workflow from master data setup to trip completion

### 2. **Transaction Documentation** (`transactions/`)
- **Cargo Registration**: Customer service entry point
- **Manifest Management**: Vehicle assignment and trip planning  
- **Trip Management**: Complete transportation execution
- **Financial Workflows**: Fund and fuel management

### 3. **API Reference** (`api/doctype-reference.md`)
- **Purpose**: Technical reference for developers
- **Content**: Complete doctype specifications, methods, and integration points

### 4. **Setup Guides** (`setup/`)
- **Master Data**: Core master data setup instructions
- **Configuration**: System configuration and settings

## 🔧 Customization

### Adding New Documentation
1. Create your markdown file in the appropriate directory
2. Update `mkdocs.yml` to include the new page in the navigation
3. Follow the existing documentation style and format

### Styling
The documentation uses the Material theme with custom CSS:
- `stylesheets/extra.css` - Additional custom styles
- `stylesheets/homepage.css` - Homepage-specific styles

### JavaScript Enhancements
Custom JavaScript files for enhanced functionality:
- `javascripts/extra.js` - General enhancements
- `javascripts/homepage.js` - Homepage-specific functionality

## 📝 Writing Guidelines

### Markdown Format
- Use standard Markdown syntax
- Include proper headings (H1, H2, H3)
- Use code blocks for technical content
- Include links to related documentation

### Content Structure
- **Overview**: Brief description of the topic
- **Purpose**: What the feature/process accomplishes
- **Step-by-step Instructions**: Clear, numbered steps
- **Examples**: Code examples and screenshots
- **Best Practices**: Recommendations and tips

### Images and Assets
- Store images in the `assets/` directory
- Use descriptive filenames
- Optimize images for web (compress if needed)
- Include alt text for accessibility

## 🌐 Deployment

### GitHub Pages
The documentation can be deployed to GitHub Pages using GitHub Actions. The workflow is configured in `.github/workflows/`.

### Other Platforms
The built documentation can be deployed to any static hosting service:
- Netlify
- Vercel
- AWS S3
- Any web server

## 🔍 Search and Navigation

The documentation includes:
- **Full-text search** across all pages
- **Table of contents** on each page
- **Previous/Next navigation**
- **Breadcrumb navigation**
- **Section navigation**

## 📊 Analytics

Google Analytics is configured (if `GOOGLE_ANALYTICS_KEY` environment variable is set) to track:
- Page views
- Search queries
- User behavior
- Documentation effectiveness

## 🤝 Contributing

To contribute to the documentation:

1. **Fork** the repository
2. **Create** a feature branch
3. **Make** your changes following the writing guidelines
4. **Test** locally using `mkdocs serve`
5. **Submit** a pull request

### Review Process
- Documentation changes are reviewed for:
  - Accuracy and completeness
  - Clarity and readability
  - Consistency with existing style
  - Technical correctness

## 📞 Support

For documentation issues or questions:
- **GitHub Issues**: [Create an issue](https://github.com/nelsonmpanju/vsd_fleet_ms/issues)
- **Email**: [nelsonnorbert87@gmail.com](mailto:nelsonnorbert87@gmail.com)

## 📄 License

This documentation is licensed under the same license as the main project (GNU General Public License v3.0).

---

**Last Updated**: December 2024  
**Version**: 1.0.0 