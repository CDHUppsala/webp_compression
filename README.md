# WebP Compression Script (Surgical JPEG Migration)

This project contains a Python script designed for the selective ("surgical") compression of high-resolution images into the WebP format. It is specifically tailored for large-scale archival databases where certain prefixes or file types are prioritized.

## Script Overview: `webpcompress.py`

The script `webpcompress.py` automates the migration of legacy image formats (JPEG, TIFF, NEF) to WebP to reduce storage footprint while maintaining visual quality.

### Technical Details

#### 1. Configuration
The script uses several hardcoded configuration variables at the top:
- `input_csv`: Path to the source metadata CSV (default: `./UMF_Database_image_list_1.csv`).
- `demo_folder`: The target directory where compressed images and logs will be stored (default: `./Gust_Images`).
- `sample_limit`: A safety cap on the number of processed images (default: `50,000`).
- `approved_prefixes`: (Currently commented out in code, but intended for filtering) A tuple of allowed filename prefixes.

#### 2. CSV Processing
- **Field Limit**: Increases `csv.field_size_limit` to `10,000,000` to handle extremely long archival file paths.
- **Delimiter Detection**: Automatically detects whether the CSV uses commas (`,`) or semicolons (`;`) by inspecting the first line.
- **Header Normalization**: Strips whitespace and removes BOM (`\ufeff`) from field names.

#### 3. Filtering Logic
The script applies multiple filters before processing an image:
- **Format Filter**: Only processes files ending in `.jpg`, `.jpeg`, `.tif`, or `.nef`.
- **Prefix Filter**: (Note: In the current version, `approved_prefixes` must be defined before use if enabled). It checks if the filename starts with specific database-approved prefixes.
- **Existence Check**: Verifies the source path exists locally/on the network.
- **Idempotency**: Skips conversion if the target WebP file already exists in the destination.

#### 4. Compression Process
- **Library**: Uses `PIL` (Pillow) for image handling.
- **Mode Conversion**: Automatically converts `RGBA`, `P`, `CMYK`, and `LA` modes to `RGB` to ensure WebP compatibility.
- **WebP Settings**: Saves images with a quality setting of `80`.
- **Naming**: Clean names are used (stripping original extensions) so that different source formats (e.g., a `.tif` and a `.jpg` of the same object) map to the same WebP identity.

#### 5. Logging
After processing, the script generates a new mapping CSV: `UMF_Image_Migration_Log.csv`. This log includes:
- All original CSV columns.
- `New_WebP_Name`: The filename of the generated WebP.
- `Local_WebP_Path`: The full path to the compressed file.

## Requirements

- Python 3.x
- Pillow (PIL): `pip install Pillow`
- Git LFS: [Installed and initialized](https://git-lfs.github.com/) (`git lfs install`)

## Usage

1. Ensure the `input_csv` path correctly points to your database export.
2. Run the script:
   ```bash
   python webpcompress.py
   ```
3. Check the `Gust_Images/WebP_Compressed` folder for the results.
4. Review `Gust_Images/UMF_Image_Migration_Log.csv` for the migration manifest.

## Git Configuration

The project includes a `.gitattributes` file to:
- Automatically normalize line endings (`* text=auto`).
- Use **Git LFS** for image assets (`.jpg`, `.tif`, `.webp`, etc.) to keep the repository size manageable.
- Ensure consistent line endings for Python and CSV files.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
