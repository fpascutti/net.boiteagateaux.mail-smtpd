from aiosmtpd.smtp import SMTP as SMTPServer, MISSING
import asyncio
import email.parser
import email.policy
import logging
import mailbox
import os
from public import public


class MailboxLockContext:

    def __init__(self, box):
        self.mailbox = box

    def __enter__(self):
        self.mailbox.lock()
        return self.mailbox

    def __exit__(self, *args, **kwargs):
        self.mailbox.close()  # unlocks, flushes and closes


class Handler:
    def __init__(self, path):
        super().__init__()
        self.root = path

    async def handle_RCPT(self, server, session, envelope, address, rcpt_options):
        (_, _, domain) = address.partition('@')
        if domain != "mail.boiteagateaux.net":
            return "551 User not local or invalid address"
        return MISSING

    async def handle_DATA(self, server, session, envelope):
        # build message
        message = email.parser.BytesParser(
            policy=email.policy.default).parsebytes(envelope.content)
        message["X-Peer"] = str(session.peer)
        message["X-MailFrom"] = envelope.mail_from
        message["X-RcptTo"] = ", ".join(envelope.rcpt_tos)

        # handle messge for each recipient
        results = await asyncio.gather(
            *[self.handle_message(rcpt_to, message)
              for rcpt_to in envelope.rcpt_tos],
            return_exceptions=True
        )

        # check if any handler failed
        for res in results:
            if isinstance(res, Exception):
                raise res
        return "250 OK"

    async def handle_message(self, rcpt_to, message):
        with MailboxLockContext(mailbox.Maildir(
                os.path.join(self.root, rcpt_to), create=True)) as mb:
            mb.add(message)


def ensure_dir(path):
    try:
        os.mkdir(path)
    except FileExistsError:
        pass
    return path


@public
async def start(loop):
    dir = ensure_dir(os.path.join(os.getcwd(), "incoming"))
    srv = await loop.create_server(lambda: SMTPServer(Handler(dir), decode_data=False), port=8025, start_serving=True)
    return srv


@public
def cli():
    async def amain():
        loop = asyncio.get_running_loop()
        srv = await start(loop)
        await srv.wait_closed()

    # logging.basicConfig(level=logging.DEBUG)
    asyncio.run(amain())
