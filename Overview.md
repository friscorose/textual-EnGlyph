# EnGlyph Technical Deep-Dive

This document provides a comprehensive technical overview of EnGlyph's capabilities, complementing the basic installation and usage covered in the README. EnGlyph is a sophisticated terminal graphics system that leverages Unicode 16.0's "Symbols for Legacy Computing" block to create scalable text and image rendering within Textual applications.

## Architecture Overview

### The Glyxel System

EnGlyph's core innovation is the "glyxel" system—a portmanteau of "glyph" and "pixel" that describes how terminal cells are subdivided into addressable display units. Each terminal character cell can be partitioned into a grid of sub-pixels using specialized Unicode characters.

**Available Basis Configurations:**

- **2×4 (Default)**: Eight glyxels per cell using octant characters like `𜴀`, `𜴁`, `𜵀`. Optimal balance of resolution and compatibility.
- **1×2 (High-fidelity)**: Two glyxels per cell using half-block characters like `▀`, `▄`. Maximum color accuracy with two distinct colors per cell.
- **2×3 (Alternative)**: Six glyxels per cell using sextant characters like `🬀`, `🬁`, `🬂`. Good resolution with moderate Unicode requirements.
- **2×2 (Quadrant)**: Four glyxels per cell using quadrant characters like `▘`, `▝`, `▀`. Legacy compatibility mode.

The basis configuration affects both rendering quality and font compatibility requirements. Higher subdivision requires more recent Unicode support.

### Unicode Dependencies

EnGlyph requires Unicode 16.0 support, specifically the "Symbols for Legacy Computing" block (U+1FB00–U+1FBFF). This dependency means your terminal and font must support these relatively new Unicode additions. Known compatible fonts include:

- Cascadia Code v2404.3+
- GNU Unifont v16.0+
- Iosevka v13.9.1+

## EnGlyphText: Advanced Scalable Typography

Beyond the basic text scaling shown in the README, EnGlyphText offers sophisticated typography control.

### Custom Font Integration

```python
from textual_englyph import EnGlyphText

# Using custom bitmap fonts
yield EnGlyphText(
    "Custom Typography",
    font_name="GohuFontuni11NerdFont-Regular.ttf",
    font_size=11,
    basis=(2, 4)
)
```

EnGlyphText leverages PIL's font rendering system, allowing integration of any TrueType or bitmap font. Bitmap fonts are recommended for terminal display as they maintain crisp edges at small sizes.

### Rich Markup Integration

EnGlyphText fully supports Rich markup syntax for inline styling:

```python
yield EnGlyphText(
    "Hello [red]colored[/] [bold]bold[/] text!",
    text_size="large"
)
```

### Performance Considerations

The core text rendering pipeline in `toglyxels.py` has been optimized for performance by directly accessing Textual's internal data structures rather than using function wrappers. The `_colors2rgb4sty()` method uses a fast RGB centroid calculation, though there remains room for improvement in color quantization algorithms.

## EnGlyphImage: Advanced Image Rendering

EnGlyphImage converts bitmap images into terminal-displayable glyxel representations using sophisticated quantization techniques.

### Color Quantization Process

Each glyxel cell can only display two colors (foreground and background). EnGlyphImage handles this limitation through:

1. **Dual-tone quantization** using PIL's `quantize(colors=2)` method
2. **Color centroid calculation** for consistent color mapping across cell boundaries
3. **Basis-aware dithering** that respects glyxel boundaries

### Advanced Configuration Options

```python
from textual_englyph import EnGlyphImage

# High-fidelity image with 1x2 basis for maximum color accuracy
yield EnGlyphImage(
    "detailed_photo.jpg",
    basis=(1, 2),  # Use half-blocks for better color representation
    id="hifi_image"
)

# Alternative sextant-based rendering
yield EnGlyphImage(
    "artwork.png",
    basis=(2, 3),  # Use sextants for 6-glyxel subdivision
    id="sextant_image"
)
```

### CSS Integration

EnGlyphImage respects Textual's CSS sizing constraints while preserving aspect ratios:

```css
#my_image {
    height: 20;
    max-width: 80;
    border: solid white;
}
```

## EnSevSeg: Seven-Segment Display Widget

One of EnGlyph's most specialized widgets is `EnSevSeg`, which renders text using seven-segment display aesthetics. This widget demonstrates advanced Unicode manipulation and custom font integration.

### Basic Seven-Segment Display

```python
from textual_englyph import EnSevSeg

# Standard alphanumeric display
yield EnSevSeg("Hello Textual", id="display")

# Numeric display with custom styling  
yield EnSevSeg("3.14159", id="pi_display", basis=(1, 2))
```

### Direct Segment Control

EnSevSeg supports direct hardware-style segment control using Private Use Area Unicode characters (U+ED00–U+EDFF):

```python
# Each character directly controls segment states
# Bits 0-6 control segments a-g, bit 7 controls decimal point
yield EnSevSeg("\uED3F \uED06 \uED5B", id="direct_control")
```

**Segment Mapping:**
- Bit 0 (LSB): Segment A (top)
- Bit 1: Segment B (top-right) 
- Bit 2: Segment C (bottom-right)
- Bit 3: Segment D (bottom)
- Bit 4: Segment E (bottom-left)
- Bit 5: Segment F (top-left)
- Bit 6: Segment G (middle)
- Bit 7: Decimal point

For example, `\uEDCF` (207 decimal) displays the number "8" with decimal point.

### Custom Seven-Segment Font

EnSevSeg includes a custom bitmap font (`EnSevSeg_8x5.ttf`) optimized for segment display aesthetics:

```python
# Using the bundled seven-segment font with standard text
yield EnGlyphText(
    "123 456",
    font_name="EnSevSeg_8x5.ttf",
    font_size=8,
    basis=(2, 4)
)
```

### Interactive Clock Example

The testing code demonstrates a complete digital clock implementation:

```python
class ClockApp(App):
    DEFAULT_CSS = """
    #clock {
        margin: 1;
        #hours { border-right: none; }
        #minutes { border-left: none; }
        #colon {
            color: red;
            background: #400000;
            border-top: outer black;
            border-bottom: outer black;
        }
    }
    """
    
    def compose(self) -> ComposeResult:
        with Horizontal(id="clock"):
            yield EnSevSeg("12", id="hours")
            yield EnGlyphText("[blink]:", text_size="small", id="colon")
            yield EnSevSeg("34", id="minutes")
```

## EnGlyphSprite: Animated Graphics

EnGlyphSprite provides frame-based animation capabilities for terminal applications, supporting both static images and multi-frame sequences.

### Multi-Frame Animation Setup

```python
from textual_englyph import EnGlyphSprite

# Single image sprite (static)
sprite = EnGlyphSprite("character_idle.png", id="character")

# Multi-frame animation sequence
animation_frames = [
    "character_idle.png",
    "character_walk1.png", 
    "character_walk2.png",
    "character_walk1.png"
]
animated_sprite = EnGlyphSprite(animation_frames, id="walker", basis=(2, 3))
```

### Frame Control and Animation

EnGlyphSprite provides programmatic frame control:

```python
class AnimatedApp(App):
    def compose(self) -> ComposeResult:
        yield EnGlyphSprite(self.animation_frames, id="sprite")
    
    def on_key(self, event):
        # Advance to next frame on keypress
        sprite = self.query_one("#sprite")
        sprite.next_frame()
        
        # Set timer for automatic frame advancement
        self.set_timer(0.5, sprite.next_frame)
```

### Interactive Animation Example

The KeyPopper demo shows sophisticated animation interaction:

```python
class InteractiveDemo(App):
    CSS = """
    EnGlyphSprite {
        height: 10;
        position: relative;
        offset: 70vw 70vh;
        opacity: 60%;
    }
    .bubble {
        position: absolute;
        offset: 50vw 0;
        background: white 20%;
        padding-left: 2;
        padding-right: 2;
    }
    """
    
    def on_key(self, event):
        # Create dynamic text overlay
        bubble = EnGlyphText(
            event.key, 
            classes="bubble", 
            text_size="large", 
            basis=(2, 3)
        )
        
        # Animate sprite response
        sprite = self.query_one("#sprite")
        sprite.next_frame()
        
        # Mount text bubble with automatic removal
        self.mount(bubble)
        self.set_timer(2.33, bubble.remove)
        self.set_timer(0.33, sprite.next_frame)
```

This creates responsive animations where characters react to user input with both sprite animation and dynamic text bubbles.

## CSS Integration and Styling

EnGlyph widgets integrate seamlessly with Textual's CSS system, supporting all standard layout and styling properties.

### Layout Controls

```css
EnGlyphText {
    align: center middle;
    margin: 2;
    padding: 1;
}

EnGlyphImage {
    height: 100%;
    max-width: 50vw;
    border: solid cyan;
}

EnSevSeg {
    background: black;
    color: lime;
    border: round white;
}
```

### Color and Effects

```css
#neon_text {
    color: cyan 80%;
    text-shadow: 0 0 cyan;
    background: black;
}

#glitch_image {
    opacity: 75%;
    filter: saturate(150%);
}
```

### Animation Support

CSS animations work with EnGlyph widgets:

```css
@keyframes pulse {
    0% { opacity: 100%; }
    50% { opacity: 30%; }
    100% { opacity: 100%; }
}

#pulsing_display {
    animation: pulse 2s infinite;
}
```

## Performance Optimization

### Rendering Pipeline

EnGlyph's rendering pipeline has been optimized at several levels:

1. **Direct Textual integration**: The `toglyxels.py` module bypasses high-level Textual APIs to directly manipulate Strip and Segment objects for better performance.

2. **Efficient color calculation**: The `_colors2rgb4sty()` method uses integer arithmetic for fast RGB centroid calculation, though more sophisticated color matching algorithms could improve quality.

3. **Memory management**: Image data is processed in chunks to minimize memory usage for large images.

### Performance Tuning

For optimal performance:

- Use basis=(1,2) for maximum color fidelity but slower rendering
- Use basis=(2,4) for balanced performance and quality
- Cache frequently-used images and fonts when possible
- Consider image pre-processing for static content

### Known Limitations

Current performance bottlenecks include:

- Color quantization could benefit from better algorithms (perceptual color distance, error diffusion dithering)
- Large image processing is memory-intensive
- Font rendering doesn't cache glyph masks between similar calls

## Advanced Usage Patterns

### Dynamic Content Updates

```python
class DynamicDisplay(App):
    def on_mount(self):
        # Update seven-segment display periodically
        self.set_interval(1.0, self.update_time)
    
    def update_time(self):
        import datetime
        now = datetime.datetime.now()
        time_str = now.strftime("%H%M")
        self.query_one("#clock").update(time_str)
```

### Mixed Widget Compositions

```python
def compose(self) -> ComposeResult:
    with Horizontal():
        # Combine different EnGlyph widgets
        yield EnGlyphImage("logo.png", basis=(1,2))
        with Vertical():
            yield EnGlyphText("Dashboard", text_size="large")
            yield EnSevSeg("88:88", id="time_display")
            yield EnGlyphSprite(status_animations, id="status")
```

### Custom Styling Integration

```python
# Apply Rich styles to EnGlyph widgets
from rich.style import Style

text_widget = EnGlyphText("Styled Text", text_size="medium")
text_widget.add_class("custom-style")
```

## Development and Debugging

### Feature Discovery

Some EnGlyph capabilities remain underdocumented in the testing directory. Areas for further exploration:

1. **Extended Unicode ranges**: The Private Use Area segment control system may support additional display types beyond seven-segment.

2. **Performance optimizations**: The `toglyxels.py` optimization comments suggest additional performance improvements are possible.

3. **Color space handling**: The current RGB centroid calculation could be enhanced with perceptual color spaces (LAB, LUV).

4. **Animation interpolation**: EnGlyphSprite supports discrete frame animation; smooth interpolation between frames could be added.

### Debugging Techniques

Enable Rich's traceback for better error reporting:

```python
from rich.traceback import install
install()
```

For development, inspect the generated glyxel patterns:

```python
# Debug glyxel generation
from textual_englyph.toglyxels import ToGlyxels

pane = ToGlyxels.font_pane("Test", "font.ttf", 12)
print(f"Dimensions: {pane[0]}x{pane[1]}")
print(f"Mask length: {len(pane[2])}")
```

### Contributing

When exploring EnGlyph's capabilities, focus on:

- **Basis configuration effects**: How different glyxel subdivisions affect rendering quality
- **Font compatibility**: Testing various font types and sizes  
- **Performance profiling**: Identifying bottlenecks in the rendering pipeline
- **Unicode edge cases**: Testing unusual characters and combinations

## Conclusion

EnGlyph represents a sophisticated approach to terminal graphics, providing multiple specialized widgets that leverage modern Unicode capabilities. Its architecture balances flexibility with performance, offering both simple high-level APIs and low-level control when needed.

The combination of EnGlyphText, EnGlyphImage, EnSevSeg, and EnGlyphSprite creates a comprehensive toolkit for creating visually rich terminal applications that go far beyond traditional text-based interfaces, while maintaining full integration with Textual's powerful layout and styling systems.
