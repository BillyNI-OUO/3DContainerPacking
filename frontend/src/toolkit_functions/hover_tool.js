

var hover_tool={

dragElement(elem, offsets) {
    let xOffset = offsets["x"], yOffset = offsets["y"];
    let active = false;
    let currentX, currentY, initialX, initialY;

    // prevent fast-dragging problem with background elements
    document.body.addEventListener("pointerdown", dragStart, false);
    document.body.addEventListener("pointerup", dragEnd, false);
    document.body.addEventListener("pointermove", drag, false);
    document.body.addEventListener("touchstart", dragStart, false);
    document.body.addEventListener("touchend", dragEnd, false);
    document.body.addEventListener("touchmove", drag, false);

    function dragStart(e) {
        if (e.type === "touchstart") {
            initialX = e.touches[0].clientX - xOffset;
            initialY = e.touches[0].clientY - yOffset;
        } else {
            initialX = e.clientX - xOffset;
            initialY = e.clientY - yOffset;
        }
        if (e.target === elem)
            active = true;
    }

    function dragEnd() {
        initialX = currentX;
        initialY = currentY;
        active = false;
        document.body.removeEventListener("pointerdown", dragStart, false);
        document.body.removeEventListener("pointerup", dragEnd, false);
        document.body.removeEventListener("pointermove", drag, false);
        document.body.removeEventListener("touchstart", dragStart, false);
        document.body.removeEventListener("touchend", dragEnd, false);
        document.body.removeEventListener("touchmove", drag, false);
    }

    function drag(e) {
        if (active) {
            if (e.type === "touchmove") {
                currentX = e.touches[0].clientX - initialX;
                currentY = e.touches[0].clientY - initialY;
            } else {
                currentX = e.clientX - initialX;
                currentY = e.clientY - initialY;
            }
            xOffset = currentX;
            yOffset = currentY;
            setTranslate(currentX, currentY, elem.parentElement);
        }
    }

    function setTranslate(xPos, yPos, el) {
        el.style.transform = "translate3d(" + xPos + "px, " + yPos + "px, 0)";
    }


}//end drag element
}//end hover_tool
export default hover_tool;