import yaml
from pylatex import Document, Section, NoEscape

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
    \newcommand*\icon[1]{\tikz[baseline=(char.base)]{\node[shape=circle,draw,inner sep=1pt, fill=mainblue,mainblue,text=white] (char) {#1};}}

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
            \begin{tabular}{p{0.5cm} @{\hskip 0.5cm}p{5cm}}
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
            sidebar_layout += r"\ifthenelse{\equal{"+d0+r"}{}}{}{\textsc{\Large\icon{\ "[:-1]+icon+r"}} & "+d+r"\\}"+"\n"
    sidebar_layout = sidebar_layout[:-4]+'}'

    sidebar_layout += r"""
                %\ifthenelse{\equal{\cvdate}{}}{}{\textsc{\Large\icon{\Info}} & \cvdate\\}
            \end{tabular}    

            %------------------------------------------------
            
            \ifthenelse{\equal{\aboutme}{}}{}{
                \profilesection{About me}
                \begin{flushleft}
                    \aboutme
                \end{flushleft}
            }

            %------------------------------------------------

            \profilesection{Skills}
            
            

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

    skills = data_cv['skills']
    doc.append(NoEscape(r"\skillstext{"+skills+"}"))
    doc.append(NoEscape(r"\makeprofile"))

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
            #d = dict(reversed(d.items()))

if __name__ == '__main__':
    with open('cv_data.yml', 'r', encoding='utf-8') as f:
        language = "_en"
        data_cv = yaml.safe_load(f)

        find(data_cv, language)
        #exit()

        templatecv = "templatecv"
        define_layout(templatecv, data_cv)
    
        doc = Document(documentclass=templatecv, lmodern=False, fontenc=None, inputenc=None, textcomp=False, page_numbers=False)

        data_cv['about'] = data_cv['about']['generic']
        data_cv['skills'] = data_cv['skills']['generic']        

        fill_cv(doc, data_cv)



        with doc.create(Section('Education', numbering=False)):
            the_list = r"""
            \begin{twenty} % Environment for a list with descriptions
                \twentyitem{2022-2023}{Université Paris-Saclay}{Gif-Sur-Yvette (FRA)}{Master in Systems, Signals and Image Processing}
                \twentyitem{2021-2023}{CentraleSupélec}{Gif-Sur-Yvette (FRA)}{Engineering, with mention in Control}
                \twentyitem{2018-2023}{UFSC - Universidade Federal de Santa Catarina}{Florianópolis (BRA)}{Control and Automation Engineering \\ PAM - Advanced Mathematics Program}
                \twentyitem{2021-2022}{Paris IV - Sorbonne Université}{Paris (FRA)}{Bachelor's degree in Philosophy}
                \twentyitem{2014-2017}{IFSC - Instituto Federal de Santa Catarina}{Florianópolis (BRA)}{Engineering Technician in Electronics}
                %\twentyitem{<dates>}{<title>}{<location>}{<description>}
            \end{twenty}
            """
            doc.append(NoEscape(the_list))


        resto = r"""
        
    \section*{Work Experience}

    \begin{twenty} % Environment for a list with descriptions
        \twentyitem{2020-2021}{Student Researcher in Neural Nets}{Florianópolis (BRA)}{\textit{at EMBRAPII, in partnership with Central Energia (R\&D on trading)} \\
        Worked on building, training, and evaluating LSTM networks regarding the prediction of precipitation data for energy trading
        }
        
        \twentyitem{2018-2021}{Student Researcher in Algebraic Topology}{Florianópolis (BRA)}{\textit{at IMPA (Brazilian Institute of Pure and Applied Mathematics)} \\
        Research on advanced topics related to Geometric Group Theory
        }
        
        \twentyitem{2018–2019}{Assistant Professor on Calculus}{Florianópolis (BRA)}{\textit{at the Mathematics Department, UFSC} \\
        Hosted office hours to assist undergraduate students
        }
        
        \twentyitem{2016–2017}{Intern as Web Developer}{Florianópolis (BRA)}{\textit{at Oi S.A. (third largest telecommunication company in Latin America)} \\
        Developed PHP, Shell, BASIC and Kernel scripts to automate tasks related to the management, monitoring and control of the backbone
        }
        %\twentyitem{<dates>}{<title>}{<location>}{<description>}
    \end{twenty}



    \section*{Projects}

    \begin{twentyshort} % Environment for a short list with no descriptions
        \twentyitem{2022}{Training Neural Networks with Kalman Filters}{Gif-Sur-Yvette (FRA)}{Implementation of modern control methods for training Neural Nets and use of the Kalman filter as an optimization algorithmx}
        
        \twentyitem{2022}{Exploring portfolio optimization methods, with BNP}{Gif-Sur-Yvette (FRA)}{Construction, Implementation and Evaluation of different portfolio allocation methods}

        \twentyitem{2022}{System for inform on cancer, with Health Guide AI}{Gif-Sur-Yvette (FRA)}{Testing of different recommendation algorithms for this purpose}

        \twentyitem{2021-2022}{Neural Nets: Attacks and Robustness, with SystemX}{Gif-Sur-Yvette (FRA)}{Study and implementation of some attack methods on NN systems}
        %\twentyitemshort{<dates>}{<title/description>}
    \end{twentyshort}



    \section*{Honours and Awards}

    \begin{twentyshort} % Environment for a short list with no descriptions
        \twentyitemshort{2021}{BRAFITEC}{Merit Scholarship for Double Degree in France}
        \twentyitemshort{2019}{Qualified to Final Phase}{OBMU (National University Maths Olympiad)}
        \twentyitemshort{2018}{Freshman Award}{OEI (Organization of Ibero-American States)}
        \twentyitemshort{2017}{Silver Medal}{OBMEP (National High School Mathematics Olympiad)}
        \twentyitemshort{2016}{Silver Medal}{OBMEP (National High School Mathematics Olympiad)}
        \twentyitemshort{2014}{Honourable Mention}{OBMEP (National High School Maths Olympiad)}
        %\twentyitemshort{<dates>}{<title}{description>}
    \end{twentyshort}
        """
        doc.append(NoEscape(resto))

    


    doc.generate_pdf('full', clean_tex=False, compiler='pdflatex')