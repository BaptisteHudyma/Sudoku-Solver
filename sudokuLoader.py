import cv2 as cv
import numpy as np
import imutils
from imutils.perspective import four_point_transform
from skimage.segmentation import clear_border
import tesseract_ocr


class Sudoku_Loader :
    def __init__ (self, imagePath, debug=False):
        self.okFlag = False
        self.debug = debug
        sudokuImage = cv.imread(imagePath)
        if sudokuImage is None:
            print("Could not load Sudoku image:", imagePath)
            return

        sudokuImage = cv.cvtColor(sudokuImage, cv.COLOR_RGB2GRAY)
        sudokuImage = cv.GaussianBlur(sudokuImage, (5, 5), 0)

        #binarize
        binarizedImage = self.binarize_image(sudokuImage)
        if self.debug:
            cv.imshow("Binarized Image", binarizedImage)
            cv.waitKey(0)

        #find contours
        puzzleContour = self.find_puzzle_contours (binarizedImage)
        if puzzleContour is None:
            print("No sudoku detected")
            return
        if self.debug:
            output = sudokuImage.copy()
            cv.drawContours(output, [puzzleContour], -1, (0, 255, 0), 2)
            cv.imshow("Puzzle Outline", output)
            cv.waitKey(0)

        #deskew 
        self.straightImage, self.straightGray = self.deskew_image(sudokuImage, binarizedImage, puzzleContour)
        if self.straightGray is not None:
            self.okFlag = True

    def get_sudoku_grid(self):
        if not self.okFlag or self.straightGray is None:
            return None

        stepX = self.straightImage.shape[0]//9
        stepY = self.straightImage.shape[1]//9
        
        newGrid = [0 for i in range(81)]

        for i in range(9):
            startX = max(0, int(stepX * i))
            endX = int(stepX * (i + 1.1))
            for j in range(9):
                startY = max(0, int(stepY * j))
                endY = int(stepY * (j + 1.1))
                numberCell = self.straightImage[startX:endX, startY:endY]
                numberCell = self.extract_clean_digit(numberCell)

                #OCR
                if numberCell is not None:  #actually a number
                    _, numberCell = cv.imencode('.png', numberCell)
                    number = tesseract_ocr.text_for_bytes(numberCell.tobytes(), "eng")
                    try:
                        #print(i, j, number)
                        number = int(number)
                    except ValueError:
                        continue    #detected str was not a number
                    if number < 1 or number > 9:    #range error
                        continue

                    newGrid[i * 9 + j] = number
        return newGrid


    def binarize_image(self, image):
        #binarize
        binarizedImage = cv.adaptiveThreshold(image, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 5, 2)
        binarizedImage = cv.bitwise_not(binarizedImage)

        dilateKernel = cv.getStructuringElement(cv.MORPH_CROSS,(3,3)) 
        binarizedImage = cv.dilate(binarizedImage, dilateKernel);
        return binarizedImage


    def find_puzzle_contours(self, binarizedImage):
        #grab contours ans sort them by size 
        contours = cv.findContours(binarizedImage.copy(), cv.RETR_EXTERNAL,
                cv.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)
        contours = sorted(contours, key=cv.contourArea, reverse=True)

        #find puzzle contour
        for cnt in contours:
            # approximate the contour
            peri = cv.arcLength(cnt, True)
            approx = cv.approxPolyDP(cnt, 0.02 * peri, True)
            # if our approximated contour has four points, then we can
                        # assume we have found the outline of the puzzle
            if len(approx) == 4:
                return approx
        return None

    
    def deskew_image(self, image, grayImage, puzzleContour):
        puzzle = four_point_transform(image, puzzleContour.reshape(4, 2))
        warped = four_point_transform(grayImage, puzzleContour.reshape(4, 2))
        # check to see if we are visualizing the perspective transform
        if self.debug:
            cv.imshow("Puzzle Transform", warped)
            cv.waitKey(0)
        return (puzzle, warped)


    def extract_clean_digit(self, digitImage):
        #extract a clean area containing a number from an image digitImage 

        # apply automatic thresholding to the cell and then clear any
        # connected borders that touch the border of the cell
        thresh = cv.threshold(digitImage, 0, 255,
                        cv.THRESH_BINARY_INV | cv.THRESH_OTSU)[1]
        erodeKernel = cv.getStructuringElement(cv.MORPH_CROSS,(3,3)) 
        thresh = cv.erode(thresh, erodeKernel, 2);
        thresh = cv.dilate(thresh, erodeKernel, 2);
        thresh = clear_border(thresh)
        # find contours in the thresholded cell
        cnts = cv.findContours(thresh.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        # if no contours were found than this is an empty cell
        if len(cnts) == 0:
            return None
        # otherwise, find the largest contour in the cell and create a
        # mask for the contour
        c = max(cnts, key=cv.contourArea)
        mask = np.zeros(thresh.shape, dtype="uint8")
        cv.drawContours(mask, [c], -1, 255, -1)
        # compute the percentage of masked pixels relative to the total
        # area of the image
        (h, w) = thresh.shape
        percentFilled = cv.countNonZero(mask) / float(w * h)
        if percentFilled < 0.02:
            return None
        # apply the mask to the thresholded cell
        digit = cv.bitwise_and(thresh, thresh, mask=mask)
        # check to see if we should visualize the masking step
        
        thresh = cv.dilate(thresh, erodeKernel, 1);
        

        if self.debug:
            concat = np.concatenate((digit, digitImage), axis=1)
            cv.imshow("Digit", concat)
            cv.waitKey(0)
        # return the digit to the calling function

        #cnts, _ = cv.findContours(thresh.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        #for cnt in cnts:
        #    appCnt = cv.approxPolyDP(cnt, 3, True)
        #    bndRec = cv.boundingRect(appCnt);
        #    print(bndRec)
        #    digit = digit[bndRec[0]:bndRec[1], bndRec[2]:bndRec[3]]
        #    digitImage = digitImage[bndRec[0]:bndRec[1], bndRec[2]:bndRec[3]]
        #    break
        return cv.bitwise_not( digit)

    



