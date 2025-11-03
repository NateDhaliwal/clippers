markdown_rules = {
  'bold': {'start': '**', 'end': '**'},
  'italic': {'start': '*', 'end': '*'},
  'list_element': {'start': '\n- ', 'end': '\n'},
  'blockquote': {'start': '> ', 'end': ''},
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
  'heading_6': {'start': '<h5>', 'end': '</h6>'}
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


class Clippers:
  def __init__(self, display:bool=False, display_formatted:bool=True):
    """
    Initialize the Clippers class.

    `display` sets whether the formatted version should be printed (`False` by default). It will return the value when False.

    `display_formatted` sets whether the printed formatted text will be displayed with the formatting (using ANSI) where applicable, or just the raw Markdown/HTML. `True` by default. 
    """
    self.display = display
    self.display_formatted = display_formatted
  
  def markdown(self, markdown_type:str, text_to_replace:str, full_text:str):
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
    converted_text = full_text.replace(text_to_replace, f"{markdown_rules[markdown_type]['start']}{text_to_replace}{markdown_rules[markdown_type]['end']}")
    if self.display:
      if self.display_formatted:
        try :
          print(full_text.replace(text_to_replace, f"{display_formatted_ansi[markdown_type]}{text_to_replace}{display_formatted_ansi['end']}"))
        except KeyError:
          print(converted_text)
      else:
        print(converted_text)
      return None
    return converted_text
  
  def markdown_all(self, markdown_type:str, full_text:str):
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
  
  def color(self, target_color:str, text:str, background:bool=False):
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
    else:
      return colored_text
  
  def html(self):
    pass
