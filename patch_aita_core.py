"""Patch aita_core to render URL sources as clickable links."""
import aita_core.app

f = aita_core.app.__file__
with open(f) as fh:
    content = fh.read()

old = '                            else:\n                                st.markdown(f"- {label}")'
new = (
    '                            elif src["file_path"].startswith("http"):\n'
    '                                st.markdown(f"- [{label}]({src[\'file_path\']})")\n'
    '                            else:\n'
    '                                st.markdown(f"- {label}")'
)

if old in content:
    patched = content.replace(old, new, 1)
    with open(f, "w") as fh:
        fh.write(patched)
    print("Patched aita_core/app.py: URL sources now render as links")
else:
    print("Already patched or pattern not found")
