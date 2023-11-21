css = """.gradio-container {
    width: 100vw; 
    height:100vh;
}

.Tabs {
    height: 100%;
}

.ChatBox {
    min-height: 65dvh;
}

.inputButton{
    max-width: 50px;
}

@media screen and (width <= 711px) {
    .textbox_default textarea {
        height: calc(100dvh - 259px);
    }

    div .default-token-counter {
        top: calc( 0.5 * (100dvh - 236px) ) !important;
    }

    .transparent-substring {
        display: none;
    }

    .hover-menu {
        min-width: 250px !important;
    }
}

.pretty_scrollbar::-webkit-scrollbar {
    width: 5px;
}

.pretty_scrollbar::-webkit-scrollbar-track {
    background: transparent;
}

.pretty_scrollbar::-webkit-scrollbar-thumb,
.pretty_scrollbar::-webkit-scrollbar-thumb:hover {
    background: #c5c5d2;
}

.dark .pretty_scrollbar::-webkit-scrollbar-thumb,
.dark .pretty_scrollbar::-webkit-scrollbar-thumb:hover {
    background: #374151;
}

.pretty_scrollbar::-webkit-resizer {
    background: #c5c5d2;
}

.dark .pretty_scrollbar::-webkit-resizer {
    background: #374151;
}

/*Token counter: */
.token-counter {
    position: absolute !important;
    /*position of the counter*/
    z-index: 100;
    background: var(--input-background-fill) !important;
    min-height: 0 !important;
    right: 177px;    /* Align it to the right */
}

.token-counter span {
    padding: 1px;
    box-shadow: 0 0 0 0.3em rgb(192 192 192 / 15%), inset 0 0 0.6em rgb(192 192 192 / 7.5%);
    border: 2px solid rgb(192 192 192 / 40%) !important;
    border-radius: 0.4em;
}
/*Token counter: */
.monospace textarea {
    font-family: monospace;
}

.textbox_default textarea,
.textbox_default_output textarea,
.textbox_logits textarea,
.textbox_logits_notebook textarea,
.textbox textarea {
    font-size: 16px !important;
    color: #46464A !important;
}

.dark textarea {
    color: #efefef !important;
}"""



