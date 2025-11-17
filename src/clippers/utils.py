import re

markdown_rules = {
  'bold': {'start': '**', 'end': '**'},
  'italic': {'start': '_', 'end': '_'},
  'list_element': {'start': '\n- ', 'end': '\n'},
  'blockquote': {'start': '\n> ', 'end': '\n'},
  'codeblock': {'start': '```\n', 'end': '\n```'},
  'inline_codeblock': {'start': '`', 'end': '`'},
  'heading_1': {'start': '# ', 'end': ''},
  'heading_2': {'start': '## ', 'end': ''},
  'heading_3': {'start': '### ', 'end': ''},
  'heading_4': {'start': '#### ', 'end': ''},
  'heading_5': {'start': '##### ', 'end': ''},
  'heading_6': {'start': '###### ', 'end': ''},
}

html_rules = {
  'bold': {'start': '<b>', 'end': '</b>'},
  'italic': {'start': '<i>', 'end': '</i>'},
  'list_element': {'start': '<li>', 'end': '</li>'},
  'blockquote': {'start': '<blockquote>', 'end': '</blockquote>'},
  'codeblock': {'start': '<pre><code>', 'end': '</code></pre>'},
  'inline_codeblock': {'start': '<code>', 'end': '</code>'},
  'heading_1': {'start': '<h1>', 'end': '</h1>'},
  'heading_2': {'start': '<h2>', 'end': '</h2>'},
  'heading_3': {'start': '<h3>', 'end': '</h3>'},
  'heading_4': {'start': '<h4>', 'end': '</h4>'},
  'heading_5': {'start': '<h5>', 'end': '</h5>'},
  'heading_6': {'start': '<h6>', 'end': '</h6>'}
}

display_formatted_ansi = {
  'end': '\033[0m',
  'bold': '\033[1m',
  'italic': '\033[3m',
  'underline': '\033[4m',
  'black': "\033[30m",
  'red': "\033[31m",
  'green': "\033[32m",
  'brown': "\033[33m",
  'blue': "\033[34m",
  'purple': "\033[35m",
  'cyan': "\033[36m",
  'background_black': "\033[40m",
  'background_red': "\033[41m",
  'background_green': "\033[42m",
  'background_brown': "\033[43m",
  'background_blue': "\033[44m",
  'background_purple': "\033[45m",
  'background_cyan': "\033[46m",
}

# Help from ChatGPT
def detect_markdown(text) -> list:
  markdown_type = set()  # use a set to keep things unique

  # Handle headings
  heading_matches = re.findall(r'^(#{1,6})\s', text, flags=re.MULTILINE)
  for hashes in heading_matches:
    markdown_type.add(f"heading_{len(hashes)}")

  for m_type, value_dict in markdown_rules.items():
    if m_type.startswith("heading_"):
      continue  # Already handled headings above

    if value_dict['start'] in text.strip():
      markdown_type.add(m_type)

  return list(markdown_type)


def detect_html(text) -> list:
  html_type = []

  for m_type, value_dict in html_rules.items():
    if value_dict['start'] in text.strip():
      html_type.append(m_type)

  return html_type

def is_integer(text:str|int) -> bool:
  is_int = False
  if type(text) == str:
    try:
      int(text)
      is_int = True
    except Exception:
      pass
  elif type(text) == int:
    print("Int")
    is_int = True
  
  return is_int


class Clippers:
  def __init__(self, display:bool=False, display_formatted:bool=True) -> None:
    """
    Initialize the Clippers class.

    `display` sets whether the formatted version should be printed (`False` by default). It will return the value when False.

    `display_formatted` sets whether the printed formatted text will be displayed with the formatting (using ANSI) where applicable, or just the raw Markdown/HTML. `True` by default. 
    """
    self.display = display
    self.display_formatted = display_formatted
  
  def markdown(self, markdown_type:str, text_to_replace:list, full_text:str) -> str|None:
    if markdown_type not in (
      'bold',
      'italc',
      'list_element',
      'blockquote',
      'codeblock',
      'inline_codeblock'
      ):
      raise Exception(
        "Markdown type must be either 'bold', 'italc', 'list_element', 'blockquote', 'codeblock' or 'inline-codeblock'"
        )
    converted_text = full_text
    for text in text_to_replace:
      converted_text = converted_text.replace(text, f"{markdown_rules[markdown_type]['start']}{text}{markdown_rules[markdown_type]['end']}")
    
    if self.display:
      if self.display_formatted:
        try :
          formatted_text = full_text
          for text in text_to_replace:
            formatted_text = full_text.replace(text, f"{display_formatted_ansi[markdown_type]}{text}{display_formatted_ansi['end']}")
          print(formatted_text)
        except KeyError:
          print(converted_text)
      else:
        print(converted_text)
      return None
    return converted_text
  
  def markdown_all(self, markdown_type:str, full_text:str) -> str|None:
    if markdown_type not in (
      'bold',
      'italc',
      'list_element',
      'blockquote',
      'codeblock',
      'inline_codeblock'
      ):
      raise Exception(
        "Markdown type must be either 'bold', 'italc', 'list_element', 'blockquote', 'codeblock' or 'inline_codeblock', or headings 1-6"
        )
    converted_text = f"{markdown_rules[markdown_type]['start']}{full_text}{markdown_rules[markdown_type]['end']}"
    if self.display:
      if self.display_formatted:
        try :
          print(f"{display_formatted_ansi[markdown_type]}{full_text}{display_formatted_ansi['end']}")
        except KeyError:
          print(converted_text)
      else:
        print(converted_text)
      return None
    return converted_text
  
  def color(self, target_color:str, text:str, background:bool=False) -> str|None:
    """
    Colours the specified text or applies a background. Text here cannot be displayed without the ANSI colour codes being escaped.

    To have a background, specify `background` as `True` (default `False`).
    
    Colours/background colours:
    - black
    - red
    - green
    - brown
    - blue
    - purple
    - cyan
    """
    key = target_color if not background else "background_" + target_color
    colored_text = "" 
    try:
      colored_text = f"{display_formatted_ansi[key]}{text}{display_formatted_ansi['end']}"
    except KeyError:
      raise Exception("Color not found, must be either black, red, green, brown, blue, purple or cyan.")
    
    if self.display:
      print(colored_text)
      return None
    return colored_text

  def html(self, html_type:str, text_to_replace:list, full_text:str) -> str|None:
    if html_type not in (
      'bold',
      'italc',
      'list_element',
      'blockquote',
      'codeblock',
      'inline_codeblock',
      'heading_1',
      'heading_2',
      'heading_3',
      'heading_4',
      'heading_5',
      'heading_6'
      ):
      raise Exception(
        "HTML type must be either 'bold', 'italc', 'list_element', 'blockquote', 'codeblock' or 'inline-codeblock', or headings 1-6"
        )
    
    converted_text = full_text
    if html_type == "list_element":
        converted_text_list = converted_text.split(" ")

        first = converted_text_list[converted_text_list.index(text_to_replace[0])]
        last = converted_text_list[converted_text_list.index(text_to_replace[-1])]

        converted_text_list[converted_text_list.index(text_to_replace[0])] = "<ul>" + first
        converted_text_list[converted_text_list.index(text_to_replace[-1])] = last + "</ul>"
        converted_text = " ".join(converted_text_list)
    for text in text_to_replace:
      converted_text = converted_text.replace(text, f"{html_rules[html_type]['start']}{text}{html_rules[html_type]['end']}")

    if self.display:
      if self.display_formatted:
        try :
          formatted_text = full_text
          for text in text_to_replace:
            formatted_text = full_text.replace(text, f"{display_formatted_ansi[html_type]}{text}{display_formatted_ansi['end']}")
          print(formatted_text)
        except KeyError:
          print(converted_text)
      else:
        print(converted_text)
      return None
    return converted_text

  def html_to_markdown(self, text_to_replace:str):
    html_tokens = detect_html(text_to_replace)
    for token in html_tokens:
      try:
        markdown_equiv = markdown_rules[token]
        html_equiv = html_rules[token]
        text_to_replace = text_to_replace.replace(html_equiv['start'], markdown_equiv['start'])
        text_to_replace = text_to_replace.replace(html_equiv['end'], markdown_equiv['end'])
      except KeyError:
        print(self.color("red", "Markdown token not found, skipping for now"))
    return text_to_replace

  def markdown_to_html(self, text_to_replace:str):
    markdown_tokens_text = detect_markdown(text_to_replace)
    markdown_tokens_in_use = [] # We will pop from this later
    # start_index = 0
    markdown_tokens = {}
    markdown_broken_down = []
    for t in markdown_tokens_text:
      markdown_tokens[t] = markdown_rules[t]['start'].strip()

    # Split text by lines, without any newlines
    full_text_list = text_to_replace.splitlines(keepends=True)
    result = []
    # markdown_tokens_split = list("".join(markdown_tokens.values()))

    for line_i in range(len(full_text_list)):
      line = full_text_list[line_i]
      text_list = list(line)
      codeblock_language = "<empty>"

      previous_line = full_text_list[line_i - 1]

      # If line is a ul li
      if line.startswith(("- ", "* ")):
        # Check if previous line is a ul li
        if line_i > 0 and previous_line.startswith(("- ", "* ")):
          pass
        else:
          result.append("<ul>\n")
      
      # If line is an ol li
      elif is_integer(text_list[0]) and text_list[1] == ".":
        # Check if previous line is an ol li
        if line_i > 0 and len(previous_line) > 1 and is_integer(list(previous_line)[0]) and list(previous_line)[1] == ".":
          pass
        else:
          result.append("<ol>\n")

      else:
        # Line is not an ol or ul li
        # Close ol/ul

        # Check if previous line is a ul li
        if line_i > 0 and previous_line.startswith(("- ", "* ")):
          result.append("</ul>\n")

        # Check if previous line is an ol li
        if line_i > 0 and len(previous_line) > 1 and is_integer(list(previous_line)[0]) and list(previous_line)[1] == ".":
          result.append("</ol>\n")

      # Now we start the logic to convert Markdown to HTML
      # We manipulate the `line` variable, and append it to `result` right at the end
      # We check through each line by character

      for char_i in range(len(text_list)):
        char = text_list[char_i]
        previous_char = text_list[char_i - 1]
        next_char = text_list[char_i + 1] if char_i < len(text_list) - 1 else ""


        if char_i == len(text_list) - 1 : # Last element
          continue

        # markdown_token_checks = {
        #   "bold": (char == "*" and next_char == "*") or (char == "_" and next_char == "_"),
        #   "italic": (char == "_" and next_char != "_") or (char == "*" and next_char != " " and next_char != "*")
        #   'list_element': (char == "-" and char_i == 0 and next_char == " ") or (char == "*" and char_i == 0 and next_char == " ") or (is_integer(char) and next_char == "." and char_i == 0),
        #   'blockquote': (char == ">" and char_i == 0),
        #   'codeblock': (char == "`" and char_i == 0 and next_char == "`" and text_list[char_i + 2] == "`"),
        #   'inline_codeblock': (char == "`" and next_char != "`" and previous_char == " "),
        #   'heading_1': ,
        #   'heading_2':,
        #   'heading_3':,
        #   'heading_4':,
        #   'heading_5':,
        #   'heading_6':
        # }

        # Exclude headers
        if char != "#":
          if char_i < len(text_list) - 1:
            # Bold
            if (char == "*" and next_char == "*") or (char == "_" and next_char == "_"):
              text_list[char_i] = html_rules['bold']['start'] if "bold" not in markdown_tokens_in_use else html_rules['bold']['end']
              text_list[char_i + 1] = ""
              if "bold" not in markdown_tokens_in_use:
                markdown_tokens_in_use.append("bold")
              else:
                markdown_tokens_in_use.remove("bold")
                continue
              
            # Italic
            if (char == "_" and next_char != "_") or (char == "*" and next_char != " " and next_char != "*"): # For italics with * where it is not a li
              text_list[char_i] = html_rules['italic']['start'] if "italic" not in markdown_tokens_in_use else html_rules['italic']['end']
              if "italic" not in markdown_tokens_in_use:
                markdown_tokens_in_use.append("italic")
              else:
                markdown_tokens_in_use.remove("italic")
                continue

            # List element
            if (char == "-" and char_i == 0 and next_char == " ") or (char == "*" and char_i == 0 and next_char == " ") or (is_integer(char) and next_char == "." and char_i == 0):
              text_list[char_i] = html_rules['list_element']['start']
              text_list.pop(-1) # Remove \n at the back of the list element
              text_list.append(html_rules['list_element']['end']) # Add closing tag at the back
              text_list.append("\n") # Make next li (or next line) go to newline (but not \n\n)
              text_list[char_i + 1] = ""
              if is_integer(char) and next_char == "." and char_i == 0:
                text_list[char_i + 2] = "" # Remove extra space
            
            # Blockquote
            if char == ">" and char_i == 0:
              text_list[char_i] = html_rules['blockquote']['start']
              text_list.pop(-1) # Remove \n at the back of the list element
              text_list.append(html_rules['blockquote']['end']) # Add closing tag at the back
              text_list.append("\n") # Make next li (or next line) go to newline (but not \n\n)
              text_list[char_i + 1] = " " if next_char != " " else ""

            # Codeblock
            if char == "`" and char_i == 0 and next_char == "`" and text_list[char_i + 2] == "`":
              text_list[char_i] = html_rules['codeblock']['start'] if "codeblock" not in markdown_tokens_in_use else html_rules['codeblock']['end']
              text_list[char_i + 1] = ""
              text_list[char_i + 2] = ""
              if "codeblock" not in markdown_tokens_in_use:
                markdown_tokens_in_use.append("codeblock")

                # Check if language is specified (we don't support that)
                if len(text_list) != 3 and text_list[1] == "" and text_list[2] == "" and text_list[3] != "\n": # Check if langauge is in codeblock
                  codeblock_language = "".join(text_list[2:])
                  text_list[char_i] = html_rules['codeblock']['start'] + "\n"
              else:
                markdown_tokens_in_use.remove("codeblock")
                continue

            # Inline codeblock
            if char == "`" and next_char != "`":
              text_list[char_i] = html_rules['inline_codeblock']['start'] if "inline_codeblock" not in markdown_tokens_in_use else html_rules['inline_codeblock']['end']
              if "inline_codeblock" not in markdown_tokens_in_use:
                markdown_tokens_in_use.append("inline_codeblock")
              else:
                markdown_tokens_in_use.remove("inline_codeblock")
                continue

      # For that of not 
      line = "".join(text_list).replace(codeblock_language, "") if codeblock_language not in ("<empty>", "", "\n", "\n\n") else "".join(text_list)
      
      # Now, we check through for headers
      header_length = 0
      header_hashes = ""
      for char in text_list:
        if char == "#":
          header_length += 1
          header_hashes += char # "#" character

      if header_hashes != "":
        line = line.lstrip(header_hashes + " ")
        try:
          line = html_rules[f"heading_{header_length}"]["start"] + line.rstrip("\n") + html_rules[f"heading_{header_length}"]["end"] + "\n"
        except KeyError:
          pass
      
      # Add it to `result`
      result.append(line)

    # Join all the elements of `result` together
    final_text = "".join(result)

    return final_text
