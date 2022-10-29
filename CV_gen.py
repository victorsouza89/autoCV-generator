import yaml, os
from pylatex import Document, Section, LineBreak
from pylatex.utils import italic, NoEscape

def define_layout(templatecv, data_cv):
    doc = []

    credits = r"""
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % Created based on the Twenty Seconds Resume/CV
    % LaTeX Template
    % Version 1.1 (8/1/17)
    %
    % This template has been downloaded from:
    % http://www.LaTeXTemplates.com
    %
    % Original author:
    % Carmine Spagnuolo (cspagnuolo@unisa.it) with major modifications by 
    % Vel (vel@LaTeXTemplates.com)
    %
    % License:
    % The MIT License (see included LICENSE file)
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """
    doc.append(NoEscape(credits))

    packages = r"""
    \ProvidesClass{"""+templatecv+r"""}[2017/01/08 CV class]
    \LoadClass{article}
    \NeedsTeXFormat{LaTeX2e}

    \RequirePackage[sfdefault]{ClearSans}
    \RequirePackage[T1]{fontenc}
    \RequirePackage{tikz}
    \RequirePackage{xcolor}
    \usepackage{sectsty}
    \RequirePackage[absolute,overlay]{textpos}
    \RequirePackage{ragged2e}
    \RequirePackage{etoolbox}
    \RequirePackage{ifmtarg}
    \RequirePackage{ifthen}
    \RequirePackage{pgffor}
    \RequirePackage{marvosym}
    \RequirePackage{parskip}
    \RequirePackage{fontawesome}
    \renewcommand*{\faicon}[1]{\makebox[1.5em][c]{\csname faicon@#1\endcsname}}


    \usepackage{tcolorbox}
    \newtcbox{\entoure}[1][white]{on line,
    arc=2pt,colback=#1!10!white,colframe=#1!50!black,
    before upper={\rule[-3pt]{0pt}{10pt}},boxrule=1pt,
    boxsep=3pt,left=0pt,right=0pt,top=1.5pt,bottom=0pt}
    """
    doc.append(NoEscape(packages))

    misc_conf = r"""
    \DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}
    \ProcessOptions\relax

    \definecolor{white}{RGB}{255,255,255}
    \definecolor{gray}{HTML}{4D4D4D}
    \definecolor{sidecolor}{HTML}{E7E7E7}
    \definecolor{mainblue}{HTML}{0E5484}
    \definecolor{maingray}{HTML}{B9B9B9}

    \renewcommand{\bfseries}{\color{gray}} % Make \textbf produce coloured text instead

    \pagestyle{empty} % Disable headers and footers

    \setlength{\parindent}{0pt} % Disable paragraph indentation
    """
    doc.append(NoEscape(misc_conf))

    sidebar_defs = r"""
    \setlength{\TPHorizModule}{1cm} % Left margin
    \setlength{\TPVertModule}{1cm} % Top margin

    \newlength\imagewidth
    \newlength\imagescale
    \pgfmathsetlength{\imagewidth}{5cm}
    \pgfmathsetlength{\imagescale}{\imagewidth/600}

    \newlength{\TotalSectionLength} % Define a new length to hold the remaining line width after the section title is printed
    \newlength{\SectionTitleLength} % Define a new length to hold the width of the section title
    \newcommand{\profilesection}[1]{%
        \setlength\TotalSectionLength{\linewidth}% Set the total line width
        \settowidth{\SectionTitleLength}{\huge #1 }% Calculate the width of the section title
        \addtolength\TotalSectionLength{-\SectionTitleLength}% Subtract the section title width from the total width
        \addtolength\TotalSectionLength{-2.22221pt}% Modifier to remove overfull box warning
        \vspace{8pt}% Whitespace before the section title
        {\color{black!80} \huge #1 \rule[0.15\baselineskip]{\TotalSectionLength}{1pt}}% Print the title and auto-width rule
    }

    % Define custom commands for CV info
    \newcommand{\aboutme}[1]{\renewcommand{\aboutme}{#1}}
    """

    for d in data_cv['basic_info']:
            sidebar_defs += r"\newcommand{\cv"+d+r"}[1]{\renewcommand{\cv"+d+r"}{#1}}"+r"""
            """ 

    for d in data_cv['more_info']:
            d = list(d.keys())[0]
            sidebar_defs += r"\newcommand{\cv"+d+r"}[1]{\renewcommand{\cv"+d+r"}{#1}}"+r"""
            """ 
    
    sidebar_defs += r"""
    %\newcommand{\cvdate}[1]{\renewcommand{\cvdate}{#1}}

    % Command for printing the contact information icons
    \newcommand*\icon[1]{\tikz[baseline=(char.base)]{\node[shape=circle,draw,inner sep=-1pt, fill=mainblue,mainblue,text=white] (char) {#1};}}

    % Command for printing skill progress bars
    \newcommand\skills[1]{ 
        \renewcommand{\skills}{
            \begin{tikzpicture}
                \foreach [count=\i] \x/\y in {#1}{
                    \draw[fill=maingray,maingray] (0,\i) rectangle (6,\i+0.4);
                    \draw[fill=white,mainblue](0,\i) rectangle (\y,\i+0.4);
                    \node [above right] at (0,\i+0.4) {\x};
                }
            \end{tikzpicture}
        }
    }

    % Command for printing skills text
    \newcommand\skillstext[1]{ 
        \renewcommand{\skillstext}{
            \begin{flushleft}
                #1%\foreach [count=\i] \x in {#1}{ 
                %	\x,%
                %}
            \end{flushleft}
        }
    }
    """
    doc.append(NoEscape(sidebar_defs))

    sidebar_layout = r"""
    
    \newcommand{\makeprofile}{
	\begin{tikzpicture}[remember picture,overlay]
   		\node [rectangle, fill=sidecolor, anchor=north, minimum width=9cm, minimum height=\paperheight+1cm] (box) at (-5cm,0.5cm){};
	\end{tikzpicture}

	%------------------------------------------------

	\begin{textblock}{6}(0.5, 0.2)
			
		%------------------------------------------------
		
		\ifthenelse{\equal{\cvphoto}{}}{}{
			\begin{center}
				\begin{tikzpicture}[x=\imagescale,y=-\imagescale]
					\clip (600/2, 567/2) circle (567/2);
					\node[anchor=north west, inner sep=0pt, outer sep=0pt] at (0,0) {\includegraphics[width=\imagewidth]{\cvphoto}};
				\end{tikzpicture}
			\end{center}
		}

		%------------------------------------------------

		{\huge\color{mainblue}\cvname}

		%------------------------------------------------

		{\Large\color{black!80}\cvjobtitle}

		%------------------------------------------------

            \renewcommand{\arraystretch}{1.6}
            \begin{tabular}{p{0.5cm} @{\hskip 0.25cm}p{7cm}}
            """

    for d in data_cv['more_info']:
            icon = d.pop('icon')
            d0 = list(d.keys())[0]
            try:
                typ = d.pop('href')
                if typ == "site":
                    typ = r"http://www."
                if typ == "mail":
                    typ = r"mailto:"
                d = r"\href{"+typ+r"\cv"+d0+r"}{\cv"+d0+r"}"
                d0 = r"\cv"+d0
            except:
                d0 = r"\cv"+d0
                d = d0
            sidebar_layout += r"\ifthenelse{\equal{"+d0+r"}{}}{}{\textsc{\icon{\ "[:-1]+icon+r"}} & "+d+r"\\}"+"\n"
    sidebar_layout = sidebar_layout[:-4]+'}'

    sidebar_layout += r"""
                %\ifthenelse{\equal{\cvdate}{}}{}{\textsc{\Large\icon{\Info}} & \cvdate\\}
            \end{tabular}    

            %------------------------------------------------
            
            \ifthenelse{\equal{\aboutme}{}}{}{
                \profilesection{"""+data_cv['about']['name']+r"""}
                \begin{flushleft}
                    
                    \aboutme
                \end{flushleft}
            }

            %------------------------------------------------

            \profilesection{"""+data_cv['skills']['name']+r"""}
            
            

            %\skills
            \skillstext
            %\scriptsize
            %(*)[The skill scale is from 0 (Fundamental Awareness) to 6 (Expert).]
                
            %------------------------------------------------
                
        \end{textblock}
    }
    """
    doc.append(NoEscape(sidebar_layout))

    lists_confs = r"""
    
%----------------------------------------------------------------------------------------
%	 COLOURED SECTION TITLE BOX
%----------------------------------------------------------------------------------------

% Command to create the rounded boxes around the first three letters of section titles
\newcommand*\round[2]{%
	\tikz[baseline=(char.base)]\node[anchor=north west, draw,rectangle, inner sep=2pt, minimum size=5.5mm, text height=3.6mm, fill=#2,#2,text=white](char){#1};%
}

\newcounter{colorCounter}
\newcommand{\sectioncolor}[1]{%
	{%
		\round{#1}{
			\ifcase\value{colorCounter}%
			mainblue\or%
			mainblue\or%
			mainblue\or%
			mainblue\or%
			mainblue\or%
			mainblue\or%
			mainblue\or%
			mainblue\or%
 			mainblue\or%
			mainblue\else%
			mainblue\fi%
		}%
	}%
	\stepcounter{colorCounter}%
}


\sectionfont{\color{mainblue}}

\renewcommand{\subsection}[1]{
	\par\vspace{.5\parskip}{%
		\large\color{gray} #1%
	}
	\par\vspace{.25\parskip}%
}

%----------------------------------------------------------------------------------------
%	 LONG LIST ENVIRONMENT
%----------------------------------------------------------------------------------------

\setlength{\tabcolsep}{0pt}

% New environment for the long list
\newenvironment{twenty}{%
	\begin{tabular*}{\textwidth}{@{\extracolsep{\fill}}ll}
}{%
	\end{tabular*}
}

\newcommand{\twentyitem}[4]{%
	#1&\parbox[t]{0.83\textwidth}{%
		\textbf{#2}%
		\hfill%
		{\footnotesize#3}\\%
		#4\vspace{\parsep}%
	}\\
}

%----------------------------------------------------------------------------------------
%	 SMALL LIST ENVIRONMENT
%----------------------------------------------------------------------------------------

\setlength{\tabcolsep}{0pt}

% New environment for the small list
\newenvironment{twentyshort}{%
	\begin{tabular*}{\textwidth}{@{\extracolsep{\fill}}ll}
}{%
	\end{tabular*}
}

\newcommand{\twentyitemshort}[3]{%
	#1&\parbox[t]{0.83\textwidth}{%
		#2, \textbf{#3}%
	}\\
}
    """
    doc.append(NoEscape(lists_confs))

    final_confs = r"""

%----------------------------------------------------------------------------------------
%	 MARGINS AND LINKS
%----------------------------------------------------------------------------------------

\RequirePackage[left=7.6cm,top=0.1cm,right=1cm,bottom=0.2cm,nohead,nofoot]{geometry}

\RequirePackage{hyperref}
    """
    doc.append(NoEscape(final_confs))
    
    with open(templatecv+r'.cls', 'w') as fp:
        for item in doc:
            # write each item on a new line
            fp.write("%s\n" % item)

def fill_cv(doc, data_cv):
    personal_info = ""
    for d in data_cv['basic_info']:
        personal_info += r"""
        \cv"""+d+r"{"+data_cv['basic_info'][d]+r"}"    
    for d in data_cv['more_info']:
        d0 = list(d.keys())[0]
        d1 = d[d0]
        personal_info += r"""
        \cv"""+d0+r"{"+d1+r"}" 
    doc.preamble.append(NoEscape(personal_info))
    
    aboutme = data_cv['about']
    doc.append(NoEscape(r"\aboutme{"+aboutme+r"}"))

    if isinstance(data_cv['skills'], list):
        skills = ''
        for s in data_cv['skills']:
            skills += r'\entoure{'+str(s)+'} '
    else: 
        skills = data_cv['skills']
    doc.append(NoEscape(r"\skillstext{"+skills+"}"))
    doc.append(NoEscape(r"\makeprofile"))

    for dd in data_cv['sections']:
        with doc.create(Section(dd['name'], numbering=False)):
            extra = ''
            if dd['type'] in ['awards']:
                extra = 'short'

            the_list = r"\begin{twenty"+extra+"}\n "
            for i in dd['items']:

                if dd['type']=='education':
                    i['title']=i['institution']
                    i['description'] = ''
                    if not isinstance(i['course'], list):
                        i['course'] = [i['course']]
                    for n in range(len(i['course'])):
                        c = i['course'][n]
                        i['description'] += c
                        try:
                            if data_cv['gpa']:
                                if not isinstance(i['GPA'], list):
                                    i['GPA'] = [i['GPA']]
                                i['description'] += r' \hspace*{\fill} GPA: ' + i['GPA'][n]
                        except:
                            None
                        i['description'] += r'\\'
                    i['description'] = i['description'][:-2]
                    
                elif dd['type']=='work':
                    i['description']= r"\textit{\textcolor{gray}{"+i['subtitle']+r"}} \\ "+ i['short_description']
                elif dd['type']=='projects':
                    i['description']= i['short_description']
                elif dd['type']=='awards':
                    i['description']= i['short_description']

                if extra == 'short':
                    the_list += r"\twentyitem"+extra+"{"+str(i['when'])+r"}{"+i['title']+r"}{"+i['description']+"}\n"
                else:
                    the_list += r"\twentyitem{"+str(i['when'])+r"}{"+i['title']+r"}{"+i['location']+r"}{"+i['description']+"}\n"
            the_list+=r"\end{twenty"+extra+"} \n"
            doc.append(NoEscape(the_list))

def find(d, tag):
    for k, v in list(d.items()):
        if isinstance(v, dict):
            find(d[k], tag)
        elif isinstance(v, list):
            try:
                for i in d[k]:
                    find(i, tag)
            except:
                None
        elif tag in k:
            d0 = {k[:-3] if k_ == k else k_:v for k_,v in d.items()}
            for kk, vv in list(d0.items()):
                try:
                    del d[kk]
                except:
                    None
                d[kk] = d0[kk]
            d[k[:-3]] = d.pop(k)

def generate_cv(language="_en", mode="generic", order_sections=['education', 'work', 'projects', 'awards'], order_info=['date', 'phone', 'mail', 'linkedin', 'github', 'address'], gpa=False, clean_tex=True):
    with open('cv_data'+language+'.yml', 'r', encoding='utf-8') as f:
        data_cv = yaml.safe_load(f)
        sections = {d['type']:d for d in data_cv['more_info']}
        data_cv['more_info'] = [sections[k] for k in order_info]

        templatecv = "templatecv"
        define_layout(templatecv, data_cv)
    
        doc = Document(documentclass=templatecv, lmodern=False, fontenc=None, inputenc=None, textcomp=False, page_numbers=False)

        try:
            data_cv['about'] = data_cv['about'][mode]
        except:
            data_cv['about'] = data_cv['about']['generic']
        try:
            data_cv['skills'] = data_cv['skills'][mode]        
        except:
            data_cv['skills'] = data_cv['skills']['generic']

        sections = {d['type']:d for d in data_cv['sections']}
        data_cv['sections'] = [sections[k] for k in order_sections]
        data_cv['gpa'] = gpa

        fill_cv(doc, data_cv)

  
    doc.generate_pdf('cv_'+mode+language, clean_tex=clean_tex, compiler='pdflatex')


if __name__ == '__main__':
    languages = ["_en", "_fr"]
    modes = ["generic", "comp", "controle", "math"]
    modes = ["comp"]
    order_sections = ['education', 'work', 'projects', 'awards']
    order_info = ['date', 'phone', 'mail', 'linkedin', 'github']#, 'address']
    gpa = True
    
    for language in languages:
        for mode in modes:
            generate_cv(language, mode, order_sections, order_info, gpa)
            os.remove("templatecv.cls")

# todo
# - photo on\off
# - skills as list