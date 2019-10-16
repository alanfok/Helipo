import json
class Merge:
    def mergeBlock(self,*mergeDictionary):
        blockNumber = 0
        nbTerm = 0
        nbPosting = 0
        tempMergeDiction = {}
        for key in sorted(mergeDictionary.keys()):
            nbPosting = nbPosting + len(mergeDictionary[key])
            tempMergeDiction[key] = mergeDictionary[key]
            nbTerm = nbTerm + 1
            if nbTerm % 24999 == 0:
                mergeCreatefile = "mergedBlock" + str(blockNumber) + ".json"
                with open(mergeCreatefile, 'w') as fp:
                    json.dump(tempMergeDiction, fp, sort_keys=True)
                    blockNumber = blockNumber + 1
                    tempMergeDiction = {}

        if (tempMergeDiction):
            mergeCreatefile = "mergedBlock" + str(blockNumber) + ".json"
            with open(mergeCreatefile, 'w') as fp:
                json.dump(tempMergeDiction, fp, sort_keys=True)
            tempMergeDiction = {}

        print("Term" + str(nbTerm))
        print("Posting" + str(nbPosting))