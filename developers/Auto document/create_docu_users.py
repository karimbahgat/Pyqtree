import sys
sys.path.append(r"C:\Users\BIGKIMO\GitHub\GitDoc")
import gitdoc

FILENAME = "pyqtree"
FOLDERPATH = r"C:\Users\BIGKIMO\GitHub\PyQuadTree"
OUTPATH = r"C:\Users\BIGKIMO\GitHub\PyQuadTree"
OUTNAME = "USER_MANUAL" 
EXCLUDETYPES = ["module","variable"]
gitdoc.DocumentModule(FOLDERPATH,filename=FILENAME,outputfolder=OUTPATH,outputname=OUTNAME,excludetypes=EXCLUDETYPES)
