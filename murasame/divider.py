import os

import pandas as pd

from . import CONFIG

conf = CONFIG["divider"]


class Divider(object):
    def __init__(self, df, files, base):
        self.data = df
        self.files = files
        self.base = base
        self.writers = {}

    def _setup_writer(self, outdir):
        assert self.files
        os.makedirs(outdir, exist_ok=True)

        for name in self.files.keys():
            path = os.path.join(outdir, name)
            self.writers[name] = pd.ExcelWriter(path)

    def save(self, outdir):
        self._setup_writer(outdir)

        for classname, member in self.data.groupby(self.base):
            member = member.drop(self.base, axis=1)
            for filename, classnames in self.files.items():
                if classname in classnames:
                    target = self.writers[filename]
                    break
            else:
                raise RuntimeError

            member.to_excel(target, classname, index=False)

        for w in self.writers.values():
            w.save()


def divider(df):
    div = Divider(df, conf["files"], conf["base"])
    div.save(conf["out"])
