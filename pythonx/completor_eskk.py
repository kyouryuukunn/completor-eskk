# -*- coding: utf-8 -*-

import logging, re
from completor import Completor, vim, get_encoding
from completor.compat import to_bytes, to_unicode

logger = logging.getLogger('completor')


class Eskk(Completor):
    filetype = 'skk'
    sync = True

    def _gather_candidates(self, bbase):
        gather_candidates = vim.Function('eskk#complete#eskkcomplete')

        candidates = [{
            'word': candidate[b'word'],
            'abbr': candidate[b'abbr'],
            'menu': b'[SKK]',
        } for candidate in gather_candidates(0, bbase)]
        # candidates.sort(key=lambda x: x['abbr'])
        return candidates

    def get_complete_position(self, base):
        eskk_is_enabled = vim.Function('eskk#is_enabled')
        # get_henkan_phase = vim.Function('eskk#get_preedit().get_henkan_phase')
        gather_candidates = vim.Function('eskk#complete#eskkcomplete')
        if not eskk_is_enabled() \
            or  re.search(r'[a-zA-Z]$', base):
            return -1
        return gather_candidates(1, '')

    def parse(self, base):
        if not base:
            return []

        bbase = to_bytes(base, get_encoding())
        pos = self.get_complete_position(base)
        logger.info(base)
        logger.info(pos)
        if pos < 0:
            return []

        candidates = self._gather_candidates(bbase)
        logger.info(candidates)
        for c in candidates:
            c['offset'] = pos

        return candidates
