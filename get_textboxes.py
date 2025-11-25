import ApplicationServices
from AppKit import NSWorkspace
import sys
import time

def get_ax_attribute(element, attribute):
    try:
        error, value = ApplicationServices.AXUIElementCopyAttributeValue(element, attribute, None)
        if error == 0:
            return value
    except Exception:
        pass
    return None

def is_attribute_settable(element, attribute):
    try:
        error, settable = ApplicationServices.AXUIElementIsAttributeSettable(element, attribute, None)
        if error == 0:
            return settable
    except Exception:
        pass
    return False

def get_position_size(element):
    pos = get_ax_attribute(element, ApplicationServices.kAXPositionAttribute)
    size = get_ax_attribute(element, ApplicationServices.kAXSizeAttribute)
    return pos, size

def traverse_and_find_textboxes(element, depth=0, max_depth=100):
    if depth > max_depth:
        return

    role = get_ax_attribute(element, ApplicationServices.kAXRoleAttribute)
    
    # Check if it is a text input
    # We look for specific roles or if the value is settable (editable)
    is_editable = is_attribute_settable(element, ApplicationServices.kAXValueAttribute)
    
    # Common roles for text input
    text_roles = ['AXTextArea', 'AXTextField']
    
    # If it's a text role OR it's editable (and not a container/window/scrollarea)
    # Note: Some combo boxes or other elements might be editable too.
    if role in text_roles or (is_editable and role not in ['AXWindow', 'AXScrollArea', 'AXGroup', 'AXList', 'AXOutline']):
        print("-" * 60)
        print(f"Found Editable Element")
        print(f"Role: {role}")
        
        role_desc = get_ax_attribute(element, ApplicationServices.kAXRoleDescriptionAttribute)
        if role_desc:
            print(f"Role Description: {role_desc}")

        value = get_ax_attribute(element, ApplicationServices.kAXValueAttribute)
        # Handle long values
        val_str = str(value)
        if len(val_str) > 200:
             print(f"Value: {val_str[:200]}... (truncated)")
        else:
             print(f"Value: {val_str}")
        
        placeholder = get_ax_attribute(element, 'AXPlaceholderValue')
        if placeholder:
            print(f"Placeholder: {placeholder}")
            
        pos, size = get_position_size(element)
        print(f"Position: {pos}")
        print(f"Size: {size}")
        
        title = get_ax_attribute(element, ApplicationServices.kAXTitleAttribute)
        if title:
            print(f"Title: {title}")
            
        description = get_ax_attribute(element, ApplicationServices.kAXDescriptionAttribute)
        if description:
            print(f"Description: {description}")
            
        help_text = get_ax_attribute(element, ApplicationServices.kAXHelpAttribute)
        if help_text:
            print(f"Help: {help_text}")

    # Recurse
    children = get_ax_attribute(element, ApplicationServices.kAXChildrenAttribute)
    if children:
        for child in children:
            traverse_and_find_textboxes(child, depth + 1, max_depth)

def main():
    print("Script will run in 3 seconds. Switch focus to the target window now...")
    time.sleep(3)

    # 1. Get the frontmost application
    workspace = NSWorkspace.sharedWorkspace()
    front_app = workspace.frontmostApplication()
    
    if not front_app:
        print("Could not determine frontmost application.")
        return

    print(f"Inspecting Frontmost App: {front_app.localizedName()} (PID: {front_app.processIdentifier()})")
    
    # 2. Create AXUIElement for the app
    ax_app = ApplicationServices.AXUIElementCreateApplication(front_app.processIdentifier())
    
    # 3. Get the focused window
    focused_window = get_ax_attribute(ax_app, ApplicationServices.kAXFocusedWindowAttribute)
    
    if focused_window:
        window_title = get_ax_attribute(focused_window, ApplicationServices.kAXTitleAttribute)
        print(f"Scanning focused window: '{window_title}'")
        traverse_and_find_textboxes(focused_window)
    else:
        print("No focused window found. Scanning all windows of the app...")
        windows = get_ax_attribute(ax_app, 'AXWindows')
        if windows:
            for window in windows:
                window_title = get_ax_attribute(window, ApplicationServices.kAXTitleAttribute)
                print(f"Scanning window: '{window_title}'")
                traverse_and_find_textboxes(window)
        else:
            print("No windows found to scan.")

if __name__ == "__main__":
    main()
