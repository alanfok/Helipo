import os
class FileRetrival:
    def retrivalSMGFile(self, file):
        for dirpath, dirnames, filenames in os.walk('.'):
            for f in filenames:
                if '.sgm' in f:
                    file.append(f)

    def retrivalTXTFile(self, file):
        for dirpath, dirnames, filenames in os.walk('.'):
            for f in filenames:
                if '.txt' and 'block' in f:
                    file.append(f)
