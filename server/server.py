from pygls.server import LanguageServer
from pygls.lsp.methods import (TEXT_DOCUMENT_DID_CHANGE, TEXT_DOCUMENT_DID_CLOSE, TEXT_DOCUMENT_DID_OPEN)
from pygls.lsp.types import (Diagnostic, DiagnosticSeverity, Position, Range)
import textx

turtle_meta = textx.metamodel_from_file("turtle.tx")

server = LanguageServer()

@server.feature(TEXT_DOCUMENT_DID_CHANGE)
def did_change(ls, params):
    validate(ls, params)

@server.feature(TEXT_DOCUMENT_DID_OPEN)
def did_open(ls, params):
    validate(ls, params)

def validate(ls, params):
    ls.show_message_log('Validating program...')

    text_doc = ls.workspace.get_document(params.text_document.uri)

    source = text_doc.source
    diagnostics = []
    try:
        turtle_meta.model_from_str(source)
    except textx.exceptions.TextXError as err:
        diagnostics.append(Diagnostic(
            range=Range(
                start=Position(line=err.line - 1, character=err.col - 1),
                end=Position(line=err.line - 1, character=err.col)
            ),
            message=err.message,
            severity=DiagnosticSeverity.Error,
            source=type(server).__name__))

    ls.publish_diagnostics(text_doc.uri, diagnostics)


server.start_ws('localhost', 3001)
