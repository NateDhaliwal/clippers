from utils import Clippers, detect_html, detect_markdown

c = Clippers()

# print(c.html("list_element", ["quickly", "lazy"], "the quick brown fox quickly jumps over the lazy dog"))

# print(detect_markdown("""I ***know*** of a person I can:
# - tell
# - report
# to in case I need to say:
#  > This is serious. What about:
# ## A header
# ### Heading 3
# # Heading 1"""))
# print(detect_html("I <b>know</b> of someone you can <i>see</i> with your own <code>eyes</code>. <h1>A header</h1>"))

# print(c.html_to_markdown("I <b>know</b> of someone you can <i>see</i> with your own <code>eyes</code>. <h1>A header</h1>"))

text = """I **know** of a __person__ I can:

- tell

- report

to in case I need to say:
> This is serious. What about:
## A header
### Heading 3
# Heading 1
"""

print(detect_markdown(text))
print(c.markdown_to_html(text))