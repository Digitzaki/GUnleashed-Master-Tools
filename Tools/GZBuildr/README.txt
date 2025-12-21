# GZBuildr - Bundle Manager

A GUI tool for parsing, extracting, and rebuilding Wii/GameCube/PS2 bundle files used in Pipeworks games.

## Supported Formats

- **.BDG** - Wii bundle files (Unleashed)
- **.CMG** - DAMM bundle files
- **.CMP** - PS2 bundle files (STE, Unleashed)
- **.CLP** - PS2 bundle files
- **.BDP** - PS2 bundle files
- **.VOL** - PS2 VOL format (experimental, view only)

## How to Use

### 1. Parse a Bundle File

**Option A: Drag and Drop** 
- Drag a `.BDG`, `.CMG`, `.CMP`, `.CLP`, `.BDP` file into the input field

**Option B: Browse**
- Click the "Browse" button
- Select your bundle file
- Click "Parse File"

The tool will display all files contained in the bundle with their:
- File number
- File name
- Offset
- Size

### 2. Extract Files

1. Click the "Extract" button after parsing
2. A new window will open showing all files grouped by type
3. Click on a category to expand it
4. Use the checkboxes to select files to extract:
   - Check individual files
   - Use "Select All in Category" for a specific type
   - Use "Select All" to extract everything
5. Click "Extract Selected"
6. Choose an output directory
7. Files will be extracted with their original folder structure (organized by type)

### 3. Rebuild a Bundle

After parsing, click the "Rebuild" button to modify and rebuild the bundle.

#### Rebuild Steps:

1. **Select Replacement Files Directory**
   - Click "Browse" under "Replacement Files Directory"
   - Choose the folder containing your modified files
   - Files must have the **exact same names** as in the original bundle

2. **Select Output Location**
   - Click "Browse" under "Output Bundle File"
   - Choose where to save the rebuilt bundle
   - Select the appropriate file extension (.BDG, .CMG, .CMP, etc.)

3. **Configure Block Alignment** ⚠️ **IMPORTANT**
   - The tool will automatically set default alignment values based on the file extension
   - These values control how files are aligned in memory:
     - **BDG** (Wii): Static/Rigged Mesh: 512, Texture: 128
     - **CMG** (DAMM): Static/Rigged Mesh: 64, Texture: 64
     - **CMP/BDP/CLP** (PS2): Static/Rigged Mesh: 128, Texture: 64

   **Manual Adjustments:**
   - If the rebuilt file doesn't work properly in-game, you may need to adjust these values
   - Common alignment values: 16, 32, 64, 128, 256, 512, 1024, 2048
   - Different file types (meshes, textures, materials) may require different alignments
   - Trial and error may be needed for specific games/platforms

4. **Click "Rebuild Bundle"**
   - The Status window will show progress
   - Files that are being replaced will be noted
   - Files not found in the replacement directory will use originals

#### Important Notes for Rebuilding:

- **Texture Files (Type 9):**
  - Size changes may indicate missing mipmaps
  - Missing mipmaps can cause low-resolution rendering at distance

- **File Size Limits:**
  - **PS2 CMP files for Save The Earth**: Maximum 2,130KB
  - Unleashed PS2 does NOT have this limit

## File Type Reference

The tool organizes files by type ID:

| Type | Description |
|------|-------------|
| 0 | Static Mesh |
| 1 | Skeleton |
| 4 | Animation |
| 6 | Material |
| 9 | Texture |
| 13 | Palette |
| 16 | PWK File |
| 17 | Rigged Mesh |
| 20 | Particle |
| 22 | PRX File |
| 23 | Localization |
| 24 | Archive |
| 25 | Audio (MIC format) |
| 26 | BDP File |
| 27 | Video (PSS format) |

## Troubleshooting

### Rebuilt file crashes or has graphical glitches
- **Cause:** Incorrect block alignment values
- **Solution:** Try adjusting the block alignment settings in the Rebuild window
  - Start by doubling or halving the current values
  - Test after each change

### Model appears stretched or deformed
- **Cause:** Block Alignment for Static & Rigged Meshes are incorrect.
- **Solution:** Please adjust these values during Rebuild.

### Textures appear low-resolution
- **Cause:** Missing mipmap data
- **Solution:** Ensure your texture replacement includes all mipmap levels

### Drag-and-drop not working
- **Cause:** `tkinterdnd2` not installed
- **Solution:** Run `pip install tkinterdnd2` or use the Browse button

### File too large for Save The Earth (PS2)
- **Cause:** CMP file exceeds 2,130KB limit
- **Solution:** Remove or reduce size of some assets
- Note: This is not a PS2 Hardware issue, as Unleashed PS2 exceeds said limit.

## Tips

- Always back up your original files before rebuilding
- Parse the bundle first to see the exact file structure
- Use identical filenames when creating replacement files
- Test rebuilt bundles thoroughly in-game
- Keep note of successful alignment settings for future mods

## Credits

Tool developed for modding Pipeworks games including:

- Godzilla: Destroy all Monsters Melee
- Godzilla: Save the Earth (PS2)
- Godzilla: Unleashed (Wii & PS2)

Note: Each game has virtually no size limit with exception to Save the Earth, which has an engine limit of 2130 KB bundle size.
