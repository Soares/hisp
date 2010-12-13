" Hisp syntax file
" Language:    Hisp
" Maintainer:  Nathanel Soares <nate@natesoares.com>
" Last Change: Dec 11, 2010
" Version:     1
" URL:	       http://hisp.natesoares.com

" ---------------------------------------------------------------------

set ignorecase
syn case ignore

runtime! syntax/html.vim
syn include @htmlJavaScript syntax/javascript.vim

syn keyword hispTodo contained TODO FIXME XXX NOTE

syn region hispNativeComment start="{!" end="!}" skip="\\\\\|\\!" keepend contains=hispTodo containedin=@hispAll
syn region hispDjangoComment start="{#" end="#}" skip="\\\\\|\\#" contains=hispTodo
syn region hispHtmlComment start="(!" end="!)" skip="\\\\\|\\!" contains=hispTodo
syn cluster hispLiveComment contains=hispDjangoComment,hispHtmlComment
syn cluster hispAll contains=@hispLiveComment

syn region hispDoctype start="(\~" end=")"
syn region hispElement matchgroup=hispDelimTag start="(\s*\(#\@=\|\.\@=\|\w\|-\)\+" end=")" contains=hispAttribute,@hispConstant,@hispStatement
syn region hispSelfCloser matchgroup=hispDelimTag start="(\/\s*\(#\@=\|\.\@=\|\w\|-\)\+" end=")" contains=hispAttribute,hispDjangoComment
syn cluster hispTag contains=hispElement,hispSelfCloser

syn region hispMacro matchgroup=hispDelimMacro start="(%\s*\(#\@=\|\.\@=\|\w\|-\)\+" end=")" contains=hispMacroExtend,hispAttribute,hispElem,hispCloser,hispBlock,hispVariable,hispHtmlComment,hispDjangoComment,hispCdata
syn region hispJavaScript keepend matchgroup=hispNewlang start="(%javascript\s\+<" end=">\s*)" skip="\\\\\|\\>" contains=@htmlJavascript
syn region hispCSS keepend matchgroup=hispNewlang start="(%css\s\+<" end=">\s*)" skip="\\\\\|\\>" contains=@htmlCss
syn cluster hispMacros contains=hispMacro,hispJavaScript,hispCSS

syn region hispBlock start="{%" end="}" skip="\\\\\|\\}\|\\\~" contains=hispBlockExtend,hispString
syn cluster hispStatement contains=hispDoctype,@hispLiveComment,@hispTag,@hispMacros
syn cluster hispAll add=@hispStatement

syn region hispBlockExtend matchgroup=hispDelimExtend start="\~" end="}\@=" contained contains=@hispConstant,@hispStatement
syn region hispBlockString matchgroup=hispDelimExtend start="\~" end="}\@=" contained contains=@hispConstant,@hispStatement
syn region hispString start=+"+ end=+"+ skip="\\\\\|\\\"" contains=hispVariable,@Spell
syn region hispAttribute matchgroup=hispDelimAttr start="(:\(\w\|-\)\+" end=")" contained contains=@hispConstant,hispDjangoComment

syn match hispClassAttr "\s\@<!\.\(\w\|-\)\+" contained containedin=@hispTag,@hispMacros
syn match hispIdAttr "\s\@<!#\(\w\|-\)\+" contained containedin=@hispTag,@hispMacros
syn cluster hispTagAttr contains=hispClassAttr,hispIdAttr
syn cluster hispAll add=@hispTagAttr

syn region hispString start=+"+ end=+"+ skip="\\\\\|\\\"" contains=hispVariable,@Spell
syn region hispLiteral start=+'+ end=+'+ skip="\\\\\|\\\'" contains=@Spell
syn region hispCDATA start="<" end=">" skip="\\\\\|\\>"
syn cluster hispText contains=hispString,hispLiteral,hispCDATA

syn region hispVariable matchgroup=hispDelimVar start="{[!#%]\@!" end="}" skip="\\\\\|\\}"
syn cluster hispDjango contains=hispDjangoComment,hispBlock,hispVariable
syn cluster hispConstant contains=@hispText,hispVariable
syn cluster hispAll add=@hispConstant

syn match hispEscapeBang +\(\\!\|\\\\\)+ contained containedin=hispNativeComment,hispHtmlComment
syn match hispEscapeHash +\(\\#\|\\\\\)+ contained containedin=hispDjangoComment
syn match hispEscapeStr +\(\\"\|\\\\\)+ contained containedin=hispString,hispBlockString
syn match hispEscapeLit +\(\\'\|\\\\\)+ contained containedin=hispLiteral
syn match hispEscapeBrak +\(\\}\|\\\\\)+ contained containedin=hispVariable
syn match hispEscapeParen +\(\\)\|\\\\\)+ contained containedin=hispVariable
syn match hispEscapeBlock +\(\\}\|\\\~\|\\\\\)+ contained containedin=hispBlock
syn match hispEscapeCDATA +\(\\>\|\\\\\)+ contained containedin=hispCDATA,hispJavaScript,hispCSS
syn cluster hispEscape contains=hispEscapeStr,hispEscapeLit,hispEscapeVar,hispEscapeBlock,hispEscapeCDATA

hi! link hispTodo Todo

hi! link hispClassAttr PreProc
hi! link hispIdAttr Identifier

hi! link hispHtmlComment PreProc
hi! link hispNativeComment Comment
hi! link hispDjangoComment Comment

hi! link hispDoctype PreProc
hi! link hispDelimTag Statement
hi! link hispDelimMacro Identifier
hi! link hispBlock PreProc

hi! link hispDelimAttr Type

hi! link hispDelimVar PreProc
hi! link hispString String
hi! link hispLiteral String
hi! link hispCDATA String

hi! link hispAttrParens Type
hi! link hispAttribute Constant

hi! link hispDelimExtend Statement
hi! link hispEscapeStr Special
hi! link hispEscapeVar Special
hi! link hispEscapeLit Special
hi! link hispEscapeBlock Special
hi! link hispEscapeCDATA Special
hi! link hispEscape Special
