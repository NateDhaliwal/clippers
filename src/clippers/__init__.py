from utils import Clippers, detect_html, detect_markdown, is_integer

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


print(c.markdown_to_html(
"""
I **know** of a _person_ I can do **that** and what else?:

- tell
- **report**

to in case I need to say:

> This is serious. What this
> to sya

1. Item
2. Another item

```
this is some code
```

So here, I have a variable called `hello`, but what does it mean?

## A header _hi_
### Heading 3
# Heading 1
"""
))
