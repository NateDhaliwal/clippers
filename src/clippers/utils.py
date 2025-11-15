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
    start_index = 0
    markdown_tokens = {}
    for t in markdown_tokens_text:
      markdown_tokens[t] = markdown_rules[t]['start'].strip()

    # Scan text from left to right
    full_text_list = text_to_replace.strip().split("\n")
    # markdown_tokens_split = list("".join(markdown_tokens.values()))
    for line in full_text_list:
      text_list = list(line)
      for char_i in range(0, len(text_list)):
        char = text_list[char_i]
        # Add HTML closing tag for tokens without specific closing on newlines (>, -)
        if char == "\n":
          if len(markdown_tokens_in_use) > 0:
            text_list[char_i] = html_rules[markdown_tokens_in_use[0]]['end']
            markdown_tokens_in_use.remove(markdown_tokens_in_use[0])
            text_list[char_i + 1] = "\n"
  
        if char != "#": # Exclude headers
          double_token = char.strip() + char.strip() if char.strip() != ">" and char.strip() != "-" and char.strip() != "_" else char.strip()

          if double_token in markdown_tokens.values():
            token_key = list((t for t, v in markdown_tokens.items() if v == double_token))[0]
            # Other Markdown token is after

            # Check if open HTML tag exists
            if token_key in markdown_tokens_in_use:
              text_list[char_i] = html_rules[token_key]['end']
              if len(double_token) == 2:
                text_list[char_i + 1] = ""
              markdown_tokens_in_use.remove(token_key)
            else:
              text_list[char_i] = html_rules[token_key]['start']
              if len(double_token) == 2:
                text_list[char_i + 1] = ""
              markdown_tokens_in_use.append(token_key)
        else:
          # Deal with headers here
          pass
       
      print("".join(text_list))
    return ""