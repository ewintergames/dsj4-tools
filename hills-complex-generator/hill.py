import numpy as np
eps = 0.00001
"""# Aerodynamic data"""

angles = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20,
          22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44]
kw_pts = [[0.00185, 0.00204, 0.00223, 0.00243, 0.00261, 0.00281, 0.00301, 0.00319,
           0.00338, 0.00355, 0.00372, 0.00388, 0.00403, 0.00418, 0.00432, 0.00447,
           0.00462, 0.00479, 0.00502, 0.00537, 0.00614, 0.00691, 0.00767],
          [0.00232, 0.00245, 0.00258, 0.00272, 0.00285, 0.00298, 0.00311, 0.00325,
           0.00337, 0.00350, 0.00362, 0.00374, 0.00386, 0.00398, 0.00410, 0.00422,
           0.00436, 0.00453, 0.00474, 0.00504, 0.00553, 0.00602, 0.00651],
          [0.00261, 0.00271, 0.00282, 0.00293, 0.00304, 0.00315, 0.00326, 0.00337,
           0.00347, 0.00357, 0.00367, 0.00376, 0.00386, 0.00396, 0.00407, 0.00419,
           0.00432, 0.00449, 0.00471, 0.00503, 0.00555, 0.00606, 0.00658]]

ka_pts = [[0.00093, 0.00139, 0.00185, 0.00231, 0.00275, 0.00316, 0.00354, 0.00390,
           0.00424, 0.00455, 0.00484, 0.00511, 0.00534, 0.00555, 0.00574, 0.00591,
           0.00605, 0.00617, 0.00628, 0.00638, 0.00655, 0.00672, 0.00689],
          [0.00116, 0.00180, 0.00244, 0.00308, 0.00365, 0.00396, 0.00424, 0.00450,
           0.00472, 0.00492, 0.00508, 0.00522, 0.00534, 0.00543, 0.00550, 0.00555,
           0.00560, 0.00565, 0.00571, 0.00582, 0.00606, 0.00629, 0.00652],
          [0.00130, 0.00177, 0.00224, 0.00270, 0.00316, 0.00350, 0.00382, 0.00411,
           0.00436, 0.00459, 0.00479, 0.00496, 0.00510, 0.00521, 0.00531, 0.00538,
           0.00545, 0.00551, 0.00558, 0.00569, 0.00590, 0.00611, 0.00632]]

kw = [np.poly1d(np.polyfit(angles, kw_pt, 4)) for kw_pt in kw_pts]
ka = [np.poly1d(np.polyfit(angles, ka_pt, 4)) for ka_pt in ka_pts]

"""# Ski jumping hill profile

## Ski jumping hill parameters
"""


class Hill:
    def __init__(self, e, es, gates, t, gamma, alpha, r1, s, l, f, alpha_dhill, h, n, l1, l2, a, betap, beta, betal, r2, r2x, r2y, k, hs, b1, b0, bk, ba, guardrail_z1, guardrail_z2):
        self.gates = gates
        self.w = k
        self.h = h
        self.n = n
        self.alpha = np.deg2rad(alpha)
        self.beta0 = np.deg2rad(alpha_dhill)
        self.gamma = np.deg2rad(gamma)
        self.e = e
        self.f = f
        self.es = es
        self.t = t
        self.r1 = r1 / 1.21
        self.r2x = r2x
        self.r2y = r2y
        self.betaP = np.deg2rad(betap)
        self.betaK = np.deg2rad(beta)
        self.betaL = np.deg2rad(betal)
        self.s = s
        self.l1 = l1
        self.l2 = l2
        self.r2 = r2
        self.b1 = b1
        self.b2 = b0
        self.bK = bk
        self.bU = ba
        self.a = a
        self.guardrail_z1 = guardrail_z1
        self.guardrail_z2 = guardrail_z2
        self.calculate_profile()

    def calculate_profile(self):
        self.betaU = 0

        tangentE2 = np.array([np.cos(self.alpha), -np.sin(self.alpha)])
        tangentE1 = np.array([np.cos(self.gamma), -np.sin(self.gamma)])
        normalE1 = np.array([np.sin(self.gamma), np.cos(self.gamma)])
        self.E2 = -self.t * tangentE2
        
        i_d = 1.5 * self.r1 * np.sin(self.gamma - self.alpha) * np.cos(self.gamma - self.alpha)**2
        i_c = np.tan(self.gamma - self.alpha) / 3 / i_d**2
        i_f = np.tan(self.gamma - self.alpha) * i_d / 3
        self.l = i_d * (1 + 0.1 * np.tan(self.gamma - self.alpha)**2)
        self.E1 = self.E2 - i_f * normalE1 - i_d * tangentE1 
        # new_r1 = i_f / np.sin(self.gamma - self.alpha) / np.tan((self.gamma - self.alpha) * 0.5)
        # print(new_r1)
        # self.C1 = self.E2 + np.array([np.sin(self.alpha), np.cos(self.alpha)]) * new_r1
        # self.E1 = self.C1 - np.array([np.sin(self.gamma), np.cos(self.gamma)]) * new_r1
        # self.l = self.r1 * (self.gamma - self.alpha)

        self.A = self.E1 - tangentE1 * (self.e - self.l)
        self.B = self.A + tangentE1 * self.es
        self.T = np.array([0, 0])

        self.F = np.array([0, -self.s])
        self.K = np.array([self.n, -self.h])

        dbeta1 = self.betaP - self.betaK
        dbeta2 = self.betaK - self.betaL

        self.rL1 = self.l1 / dbeta1 if np.abs(dbeta1) >= eps else 0
        self.rL2 = self.l2 / dbeta2 if np.abs(dbeta2) >= eps else 0

        self.rL1 = (self.rL1 + self.rL2) * 0.5
        self.rl2 = self.rL2

        print(self.rL1, self.rL2, self.l1, self.l2)

        normalK = np.array([np.sin(self.betaK), np.cos(self.betaK)])
        normalP = np.array([np.sin(self.betaP), np.cos(self.betaP)]) 
        tangentK = np.array([np.cos(self.betaK), -np.sin(self.betaK)])
        normalL = np.array([np.sin(self.betaL), np.cos(self.betaL)]) 
        normalU = np.array([np.sin(self.betaU), np.cos(self.betaU)])

        self.CL1 = self.K + normalK * self.rL1 
        self.P = self.K - tangentK * self.l1 if self.rL1 == 0 else self.CL1 - normalP * self.rL1

        self.CL2 = self.K + normalK * self.rL2
        self.L = self.K + tangentK * self.l2 if self.rL2 == 0 else self.CL2 - normalL * self.rL2

        if self.r2x is None and self.r2y is None:
            self.C2 = self.L + normalL * self.r2
            self.U = self.C2 - normalU * self.r2
        else:
            self.U = self.L + np.array([self.r2x, -self.r2y])