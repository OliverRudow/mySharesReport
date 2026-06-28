# myReport

`myReport` is a dedicated automated reporting module designed to generate comprehensive market analysis reports in PDF format. Built on top of the `reportlab` library, it formats and visualizes financial metrics like sector changes, top industries, overall scores, and 20-day price momentums into structured tables across a landscape A4 document layout.

## Project Structure

This module coordinates directly with your file utilities and shares configuration scripts:

```text
your_package/
├── __init__.py
├── myReport.py                           # This module (PDF Generation)
├── myfilebase.py                         # Provides file system operations (MyFileBase)
└── mysharesdefinition.py                 # Provides layout & path configs (myReportTopListDefinitions)
```

## Features

* **Landscape PDF Engine**: Dynamically builds professional landscape A4 financial reports using ReportLab's flowable objects (`SimpleDocTemplate`).
* **Multi-Table Visualizations**: Features native builder methods for five key market tracking tables:
  1. Sector relative changes (%)
  2. Top Industries relative changes (%)
  3. Asset Overall Scores
  4. 20-Day baseline performance changes (%)
  5. Combined overall scores overlaid with 20-day change benchmarks
* **Adaptive Multi-Page Layouts**: Separates canvas states cleanly via event callbacks, establishing a formal cover-page header design while automatically handling page numbers and authors on subsequent pages.
* **Email-Ready Architecture**: Bundles python's secure standard mailing protocols (`smtplib`, `MIMEMultipart`) for downstream scheduled delivery tasks.

## Design Configurations

### Table Geometries
To map diverse ticker strings without clipping, column arrays employ strict predefined spacing tokens:
* **`COL_WIDTH_LARGE`**: Evaluated across 12 tracking targets `[72, 180, 140, 36, 52, 36, 36, 36, 36, 36, 36, 36]`.
* **`COL_WIDTH_LARGE_2`**: Evaluated across 9 tracking targets `[72, 180, 140, 36, 52, 36, 36, 180, 36]`.

### Palette styling
* Primary Header Background: Deep Executive Blue (`#1f4e78`)
* Alternating Row Background: Soft Minimalist Gray (`#f2f2f2`)

## Dependencies

Ensure your execution environment has the standard data and layout processing requirements installed:

```bash
pip install reportlab
```

## Quick Start

Initialize `MyReport` by setting an active working directory and defining your target output filename:

```python
from myReport import MyReport

# Initialize and assign paths via myfilebase infrastructure
report_generator = MyReport(
    str_working_directory="path/to/database", 
    str_pdf_report_filename="june_market_scan.pdf"
)

# Populate the reporting vectors manually or via your pipeline
report_generator._list_sectors = [
    ["Sector", "Change %"], 
    ["Technology", "+2.4%"], 
    ["Energy", "-1.1%"]
]

# Append flowables into the active story
report_generator._built_first_table()

# Render out your final PDF
report_generator._built_story()
```

## Module Overview

### Classes
* `MyReport`: Main controller dataclass organizing document frames, underlying matrix arrays (`_list_sectors`, `_list_industries`, etc.), typography schemas (`ParagraphStyle`), and layout geometries.

### Layout Triggers
* `on_first_page(canvas, doc)`: Canvas modifier adding large bold typography titles, structural meta-blocks, and author data at exact coordinate footprints on page 1.
* `on_later_pages(canvas, doc)`: Clean structural callback drawing runtime document paths, author footnotes, and calculated page integers on all following canvas horizons.

## License & Copyright

© 2026, Brain Center Höfen. All rights reserved.  
**Author:** Oliver Rudow (<oliver.rudow@googlemail.com>)  
**Version:** 0.1.0
