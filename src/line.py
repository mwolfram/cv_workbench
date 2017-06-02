class Line():
    def __init__(self):
        self.reset()

    def reset(self):
        # was the line detected in the last iteration?
        self.detected = False
        # confidence of measurement
        self.confidence = DEFAULT_CONFIDENCE
        # x values of the last n fits of the line
        self.recent_xfitted = []
        #average x values of the fitted line over the last n iterations
        self.bestx = None
        #polynomial coefficients averaged over the last n iterations
        self.best_fit = None
        self.best_fit_amnt = 0
        #polynomial coefficients for the most recent fit
        self.current_fit = []
        #radius of curvature of the line in some units
        self.radius_of_curvature = None
        #distance in meters of vehicle center from the line
        self.line_base_pos = None
        #difference in fit coefficients between last and new fits
        self.diffs = np.array([0,0,0], dtype='float')
        #x values for detected line pixels
        self.allx = None
        #y values for detected line pixels
        self.ally = None
        # avg number of points in a fit
        self.average_fit_points = 0.0
        # amount of fit points
        self.amnt_fit_points = []

    def addToAverageFitPoints(self, fit_points):
        self.amnt_fit_points.append(float(len(fit_points)))

        if len(self.amnt_fit_points) > HISTORY_SIZE:
            del self.amnt_fit_points[0]

        self.average_fit_points = sum(self.amnt_fit_points) / float(len(self.amnt_fit_points))

    def addToAverageBestFit(self, fit, img_shape):
        self.averageOverCurrentFit(fit, img_shape)
        #self.averageOverXFitted(fit, img_shape)

    def averageOverCurrentFit(self, fit, img_shape):
        self.current_fit.append(fit)
        if len(self.current_fit) > HISTORY_SIZE:
            del self.current_fit[0]
        sum_fit = np.zeros_like(fit)
        for prev_fit in self.current_fit:
            sum_fit += prev_fit

        self.best_fit = sum_fit / len(self.current_fit)

    def averageOverXFitted(self, fit, img_shape):

        if len(self.recent_xfitted) > HISTORY_SIZE:
            del self.recent_xfitted[0]

        # Generate x and y values for plotting
        ploty = np.linspace(0, img_shape[0]-1, img_shape[0] )
        plotx = fit[0]*ploty**2 + fit[1]*ploty + fit[2]

        self.recent_xfitted.append(plotx)

        complete_y = []
        complete_x = []
        for prev_xfitted in self.recent_xfitted:
            complete_y.extend(ploty)
            complete_x.extend(prev_xfitted)

        self.best_fit = np.polyfit(complete_y, complete_x, 2)

    def toStrings(self):
        return ["Best fit: " + str(self.best_fit),
                "Detected? " + str(self.detected),
                "CurFit length: " + str(len(self.current_fit)),
                "Xfitted length: " + str(len(self.recent_xfitted)),
                "Avg Fit Points: " + str(self.average_fit_points)]
