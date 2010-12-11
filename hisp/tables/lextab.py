# hisp.tables.lextab.py. This file automatically created by PLY (version 3.3). Don't edit!
_tabversion   = '3.3'
_lextokens    = {'COMMENT': 1, 'WORD': 1, 'NAME': 1, 'EXTEND': 1, 'OP_CLOSER': 1, 'CB': 1, 'OP_MACRO': 1, 'DOCTYPE': 1, 'OP_ATTR': 1, 'ID': 1, 'VARIABLE': 1, 'OB_BLOCK': 1, 'STRING': 1, 'CP': 1, 'CLASS': 1, 'OP': 1}
_lexreflags   = 0
_lexliterals  = ''
_lexstateinfo = {'INITIAL': 'inclusive'}
_lexstatere   = {'INITIAL': [('(?P<t_COMMENT>\\(\\s*!([^)\\\\]*(?:\\\\.[^)\\\\]*)*)\\))|(?P<t_DOCTYPE>\\(\\s*~([^)\\\\]*(?:\\\\.[^)\\\\]*)*)\\))|(?P<t_OP_ATTR>\\(\\s*:)|(?P<t_OP_MACRO>\\(\\s*%)|(?P<t_OP_CLOSER>\\(\\s*/)|(?P<t_OP>\\()|(?P<t_OB_BLOCK>\\{\\s*%)|(?P<t_EXTEND>~)|(?P<t_VARIABLE>\\{([^}\\\\]*(?:\\\\.[^}\\\\]*)*)\\})|(?P<t_CP>\\))|(?P<t_CB>\\})|(?P<t_CLASS>\\.([\\w-]+))|(?P<t_ID>\\#([\\w-]+))|(?P<t_NAME>[\\w-]+)|(?P<t_WORD>[^({~"\\s})]*[^({~"\\s\\w})][^({~"\\s})]*)|(?P<t_STRING>"([^"\\\\]*(?:\\\\.[^"\\\\]*)*)")', [None, ('t_COMMENT', 'COMMENT'), None, ('t_DOCTYPE', 'DOCTYPE'), None, ('t_OP_ATTR', 'OP_ATTR'), ('t_OP_MACRO', 'OP_MACRO'), ('t_OP_CLOSER', 'OP_CLOSER'), ('t_OP', 'OP'), ('t_OB_BLOCK', 'OB_BLOCK'), ('t_EXTEND', 'EXTEND'), ('t_VARIABLE', 'VARIABLE'), None, ('t_CP', 'CP'), ('t_CB', 'CB'), ('t_CLASS', 'CLASS'), None, ('t_ID', 'ID'), None, ('t_NAME', 'NAME'), ('t_WORD', 'WORD'), ('t_STRING', 'STRING')])]}
_lexstateignore = {'INITIAL': ' \t\n'}
_lexstateerrorf = {'INITIAL': 't_error'}
