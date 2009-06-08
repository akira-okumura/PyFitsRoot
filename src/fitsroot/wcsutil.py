"""
Part of this code is ported from AstroROOT

$Id: wcsutil.py,v 1.4 2009/06/08 15:38:53 oxon Exp $
"""
import numpy
import pyfits
import pywcs
import ROOT

def coords_out(imgx, imgy):
    """
    Original code is CoordsOut in AstroROOT
    """
    return not (ROOT.gPad.GetUxmin() <= imgx <= ROOT.gPad.GetUxmax() and \
                ROOT.gPad.GetUymin() <= imgy <= ROOT.gPad.GetUymax())

def border_coords(inx, iny, out, it=8):
    """
    Original code is BorderCoords in AstroROOT
    """
    if it <= 0:
        return

    it -= 1

    cx = (inx + out[0])/2.
    cy = (iny + out[1])/2.

    if coords_out(cx, cy):
        out[0] = cx
        out[1] = cy
        border_coords(inx, iny, out, it)
    else:
        border_coords(cx, cy, out, it)

class FitsImage(ROOT.TH2D):
    def __init__(self, fname, extension, name="", title=""):
        if type(extension) != list and type(extension) != tuple:
            hdu = pyfits.open(fname)[extension]
            ybins, xbins = hdu.data.shape
        else:
            hdu = pyfits.open(fname)[extension[0]]
            ybins, xbins = hdu.data.shape[1:]

        self.wcs = pywcs.WCS(hdu.header)
        ROOT.TH2D.__init__(self, name, title, xbins, 0.5, xbins + 0.5, ybins, 0.5, ybins + 0.5)
        if type(extension) != list and type(extension) != tuple:
            for y in range(ybins):
                for x in range(xbins):
                    self.SetBinContent(x + 1, y + 1, hdu.data[y, x])
                    self.SetBinContent(x + 1, y + 1, hdu.data[y, x])
        else:
            for y in range(ybins):
                for x in range(xbins):
                    self.SetBinContent(x + 1, y + 1, hdu.data[extension[1], y, x])
                    self.SetBinContent(x + 1, y + 1, hdu.data[extension[1], y, x])

        self.grid = []
        self.label = []
    
    def sky2bin(self, x, y):
        xy = self.wcs.wcs_sky2pix(numpy.array([[x, y],]), 1)
        return xy[0][0], xy[0][1]

    def bin2sky(self, x, y):
        xy = self.wcs.wcs_pix2sky(numpy.array([[x, y],]), 1)
        return xy[0][0], xy[0][1]

    def add_gridA(self, b, a0, da):
        self.grid.append(FitsGrid(self, 0, b, da, a0))
        return self.grid[-1]

    def add_gridB(self, a, b0, db):
        self.grid.append(FitsGrid(self, 1, a, db, b0))
        return self.grid[-1]

    def add_labelA(self, a, b, label):
        self.label.append(FitsGridLabel(self, a, b, label, 0))
        return self.label[-1]

    def add_labelB(self, a, b, label):
        self.label.append(FitsGridLabel(self, a, b, label, 1))
        return self.label[-1]

    def draw_label(self):
        """
        """
        for label in self.label:
            label.Draw()

    def draw_grid(self):
        """
        """
        uxmin = ROOT.gPad.GetUxmin()
        uxmax = ROOT.gPad.GetUxmax()
        uymin = ROOT.gPad.GetUymin()
        uymax = ROOT.gPad.GetUymax()
        limA, limB = zip(self.bin2sky(uxmin, uymin),
                         self.bin2sky(uxmax, uymin),
                         self.bin2sky(uxmax, uymax),
                         self.bin2sky(uxmin, uymax),
                         self.bin2sky((uxmin + uxmax)/2, (uymin + uymax)/2)
                        )
        limA, limB = list(limA), list(limB)

        minB = maxB = limB[0]

        for i in range(1, 4):
            minB = min(minB, limB[i])
            maxB = max(maxB, limB[i])

        pol = False

        imgx, imgy = self.sky2bin(180., 90.)

        if not coords_out(imgx, imgy):
            maxB = 89.99999999
            minA = 0.
            maxA = 360.
            pol = True

        imgx, imgy = self.sky2bin(180., -90.)

        if not coords_out(imgx, imgy):
            minB = -89.99999999
            minA = 0.
            maxA = 360.
            pol = True

        if not pol:
            diff = (limA[0] - limA[4], limA[4] - limA[2],
                    limA[1] - limA[4], limA[4] - limA[3])
            if diff[0]*diff[1] < 0. or diff[2]*diff[3] < 0.:
                minA = maxA = limA[0]
                for i in range(1, 4):
                    minA = min(minA, limA[i])
                    maxA = max(maxA, limA[i])
                for i in range(4):
                    if abs(limA[i] - minA) < abs(limA[i] - maxA):
                        limA[i] += 360.

            minA = maxA = limA[0]

            for i in range(1, 4):
                minA = min(minA, limA[i])
                maxA = max(maxA, limA[i])

            minA, maxA = minA - (maxA - minA)*0.1, maxA + (maxA - minA)*0.1
            minB, maxB = minB - (maxB - minB)*0.1, maxB + (maxB - minB)*0.1

        self.minA, self.maxA, self.minB, self.maxB = minA, maxA, minB, maxB

        for grid in self.grid:
            grid.draw()

class FitsGridLabel(ROOT.TLatex):
    def __init__(self, img, a, b, text, axis):
        self.img = img
        self.a = a
        self.b = b
        x, y = self.img.sky2bin(self.a, self.b)
        ROOT.TLatex.__init__(self, x, y, text)
        self.SetTextAlign(22)

        if axis == 0:
            da = 1e-10
            db = 0
        else:
            da = 0
            db = 1e-10

        x2, y2 = img.sky2bin(self.a + da, self.b + db)
        rot = ROOT.TMath.RadToDeg()*ROOT.TMath.ATan2(y2 - y, x2 - x)
        if rot < 0:
            rot += 180
        if rot > 180:
            rot -= 180
        self.SetTextAngle(rot)

class FitsGrid(ROOT.TAttLine):
    def __init__(self, img, coord, y, dx, x0):
        ROOT.TAttLine.__init__(self)
        self.img = img
        self.y = y
        self.dx = dx
        self.x0 = x0
        self.coord = coord
        self.pol = []

    def draw(self):
        status = 0
        xarr = numpy.zeros(100)
        yarr = numpy.zeros(100)
        prex, prey = 0, 0
        
        if self.coord == 0:
            A1 = self.img.minA
            A2 = self.img.maxA
            B1 = B2 = self.y
            dA = (A2 - A1)/99.
            dB = 0.
        else:
            A1 = A2 = self.y
            B1 = self.img.minB
            B2 = self.img.maxB
            dA = 0.
            dB = (B2 - B1)/99.

        n = 0

        for i in range(100):
            xarr[n], yarr[n] = self.img.sky2bin(A1 + dA*i, B1 + dB*i)
            out = coords_out(xarr[n], yarr[n])

            if (status == 0 or status == 3) and not out:
                status = 1
            elif status == 1 and not out:
                status = 2
            elif (status == 1 or status == 2) and out:
                status = 3
            elif status == 3 and out:
                status = 0

            if status == 0:
                prex = xarr[n]
                prey = yarr[n]
                continue
            elif status == 1 and i != 0:
                pos = [prex, prey]
                border_coords(xarr[n], yarr[n], pos)
                prex, prey = pos[0], pos[1]
                xarr[n + 1] = xarr[n]
                yarr[n + 1] = yarr[n]
                xarr[n] = prex
                yarr[n] = prey
                n += 1
            elif status == 3:
                pos = [xarr[n], yarr[n]]
                border_coords(xarr[n - 1], yarr[n - 1], pos)
                xarr[n], yarr[n] = pos[0], pos[1]

            n += 1

            if status == 3:
                self.pol.append(ROOT.TPolyLine(n, xarr, yarr))
                n = 0

        self.pol.append(ROOT.TPolyLine(n, xarr, yarr))

        for p in self.pol:
            p.SetLineColor(self.GetLineColor())
            p.SetLineStyle(self.GetLineStyle())
            p.SetLineWidth(self.GetLineWidth())
            p.Draw("C")
