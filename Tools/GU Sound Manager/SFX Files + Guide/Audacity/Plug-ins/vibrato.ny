;nyquist plug-in
;version 4
;type process
;categories "http://lv2plug.in/ns/lv2core/#Modulator"
;name "Vibrato..."
;info "by Steve Daulton (http://easyspacepro.com).\n\nIf more than one value is given for speed and/or depth,\n(separated by spaces), the supplied values will be\nevenly spaced between start and end of the selection.\n"
;action "Processing..."
;preview "enabled"
;author "Steve Daulton"
;copyright "Released under terms of the GNU General Public License version 2" 

;; vibrato.ny by Steve Daulton, Dec 2014
;; Released under terms of the GNU General Public License version 2
;; http://www.gnu.org/copyleft/gpl.html

;control hzlist "Vibrato speed" string "0 to 100 Hz" "5" ""
;control depthlist "Vibrato depth" string "0 to 100 %" "30"


(defun string-to-list (string)
"Convert a string into a list"
  (read (make-string-input-stream (format nil "(~a)" string))))

(setf hzlist (string-to-list hzlist))
(setf depthlist (string-to-list depthlist))

(defun GetBreakpoints (type data)
  (do ((i (1- (length data)) (1- i))
       (bp ())
       (intval (/ 1.0 (1- (length data)))))
    ((< i 0) (cdr bp))
  (if (= type 0)  ;Hz
      (setf val (checkHz (nth i data)))
      (setf val (checkdepth (nth i data))))
  (push val bp)
  (push intval bp)))

(defun env (type data)
  (cond
    ((and (< (length data) 1)(= type 0))  ;Hz
      (throw 'err "Error.\n'Vibrato speed' not set."))
    ((< (length data) 1)  ;depth
      (throw 'err "Error.\n'Vibrato depth' not set."))
    ((and (= (length data) 1)(= type 0))  ;Hz
      (checkHz (first data)))
    ((= (length data) 1)  ;depth
      (checkdepth (first data)))
    (T (setf bp (GetBreakpoints type data))
       (pwlvr-list bp))))

(defun checkHz (x)
  (cond
    ((not (numberp x)) (throw 'err 
      (format nil "Error.~%Value '~a' is not a number.~%~
              'Vibrato speed' values must all be numbers." x)))
    ((or (< x 0) (> x 100)) (throw 'err 
      (format nil "Error.~%Value '~a' is out of range.~%~
              'Vibrato speed' values must be between 0 and 100 Hz." x)))
    (T x)))

(defun checkdepth (x)
  (cond
    ((not (numberp x)) (throw 'err 
      (format nil "Error.~%Value '~a' is not a number.~%~
              'Vibrato depth' values must all be numbers." x)))
    ((or (< x 0) (> x 100)) (throw 'err 
      (format nil "Error.~%Value '~a' is out of range.~%~
              'Vibrato depth' values must be between 0 and 100 %" x)))
    (T (power (/ x 100.0) 3.0))))

(defun vibrato (sig)
  (let ((hz (env 0 hzlist))
        (depth (env 1 depthlist)))
    (setf map
      (integrate
        (sum (diff 1 depth)
             (mult depth
                   (sum 1 (hzosc hz))))))
    (snd-compose sig map)))

(catch 'err (multichan-expand #'vibrato *track*))