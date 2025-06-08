import streamlit as st

def page1():

    return st.markdown(
            """
            ## ❓ Why use Evidence Network Builder
            Complex analysis of probabilistic events is complicated... Whilst analysts are good at estimating probabilities over small, well understood domains, they perform badly over large ones. Moreover, they rarely an intuitive understanding of how probabilistic causal events affect eachother. Finally, using structured analytic techniques have been key to winning superforecasting teams.

            So... why not use a tool that takes your analysis, breaks it down into a set of small domains that you are good at estimating, links those domains to your hypothesis (and uses MATHS to calculate their probabilities), and enforces a structured analytical technique!             

            ## 🧠 How to use Evidence Network Builder

            **Build, explore & export networks of evidence and hypotheses.**

            1. **Import**  
            Paste your narrative or upload a JSON to auto-extract nodes via GPT, or add/edit nodes and edges manually.

            2. **Quantify**  
            Assign qualitative **priors** to hypotheses, rate **evidence reliability**, and set **edge strength** multipliers.

            3. **Analyze**  
            View calculated probabilities, truth-tables by component, and an interactive network graph.

            4. **Export**  
            Download your full network (with priors, truth-probs & weights) as JSON.

            _Select “Builder” above to get started!_
            """,
            unsafe_allow_html=True,
        )

def page2():
    """Render the full ‘Why Do Analysts Struggle…’ paper content."""
    with st.container():
        st.header("Why Do Analysts Struggle to Predict Probabilistic Events?")
        st.subheader("Abstract")
        st.markdown(
            """
            Analysts frequently encounter difficulties in accurately predicting probabilistic events due to inherent cognitive limitations and reliance on heuristic reasoning. This paper examines three interrelated factors contributing to these challenges: (1) varying predictive accuracy in small versus large domains, (2) intuitive human probability reasoning and associated systematic biases, and (3) the role and effectiveness of Structured Analytical Techniques (SATs) in addressing these biases. While humans can perform effectively in constrained environments with clear and frequent feedback, their ability to predict outcomes deteriorates significantly in complex, ambiguous contexts. SATs provide structured methods that aim to mitigate judgmental errors but require thoughtful implementation and organizational support.
            """,
            unsafe_allow_html=True,
        )
        # 1. Introduction
        st.markdown("### 1. Introduction")
        st.markdown(
            """
            Prediction is a core human activity in domains ranging from medicine to intelligence analysis. 
            However, the reliability of human judgment varies dramatically depending on the context. 
            This paper explores how domain characteristics, intuitive probability reasoning, and structured methods intersect to shape predictive performance.
            """
        )
        # 2. Small vs. Big Domains
        st.markdown("### 2. Prediction in Small vs. Big Domains")
        st.markdown(
            """Small-domain successes include meteorologists accurately forecasting short-term weather and chess masters in endgame scenarios.
            Large-domain failures include geopolitical and economic forecasts, where complexity and interacting variables lead to mispredictions.
            """
        )
        st.markdown("#### 2.1 Small Domains")
        st.markdown(
            """Small domains are characterized by stability, regular feedback, and well-understood variables.
            Expert intuition develops reliably in these environments (Kahneman & Klein, 2009).
            """
        )
        st.markdown("#### 2.2 Big Domains")
        st.write(
            "Big domains like geopolitics exhibit ambiguity, delayed feedback, and complex interactions. Experts often perform no better than chance due to overconfidence and narrative biases (Tetlock, 2005)."
        )
        # 3. Intuition for Probability
        st.markdown("### 3. Intuition for Probability")
        st.markdown(
            """Human probability intuition evolved for quick, heuristic judgments rather than precise calculations (Cosmides & Tooby, 1996).
            "While humans excel with frequency formats, they commit systematic errors like base-rate neglect, conjunction fallacy, and overestimating rare events (Kahneman & Tversky, 1973; Slovic et al., 1980).
            """
        )
        # Strengths and Biases
        st.markdown("#### 3.1 Strengths of Intuition")
        st.write(
            "Humans process frequencies (e.g., '1 in 10') more effectively than abstract probabilities (Gigerenzer & Hoffrage, 1995). Familiar contexts support pattern-based predictions."
        )
        st.markdown("#### 3.2 Systematic Biases")
        st.markdown(
            """
            Common biases include:
            • Base-rate neglect: ignoring general probabilities in favor of specifics.
            • Conjunction fallacy: rating combined events as more likely than single events.
            • Overestimating rare events: vivid scenarios inflate perceived risk.
            • Difficulty with compound probabilities: underestimating sequential odds.
            """
        )
        # 4. SATs
        st.markdown("### 4. Structured Analytical Techniques (SATs)")
        st.write(
            "SATs provide structured methods to reduce bias and improve transparency but face implementation challenges like training needs and cultural resistance."
        )
        st.markdown("#### 4.1 Purpose and Types")
        st.markdown(
            """
            Common SATs:
            • Analysis of Competing Hypotheses (ACH): test alternative hypotheses against evidence to counter confirmation bias (Heuer, 1999).  
            • Key Assumptions Check: identify and challenge underlying assumptions (Heuer & Pherson, 2010).  
            • Premortem Analysis: imagine failure and identify risks to reduce overconfidence (Klein, 2007).  
            • Red Teaming: adversarial challenge to expose blind spots (Zenko, 2015).
            """
        )
        st.markdown("#### 4.2 Evidence of Effectiveness")
        st.write(
            "ACH enhances transparency but shows mixed accuracy gains (Dhami et al., 2015). SATs reduce overconfidence and aid hypothesis testing (Chang et al., 2018), and superforecasters using structured methods outperform peers (Tetlock & Gardner, 2015); however, results depend on training and integration (McDowell & Moxley, 2016)."
        )
        # 5. Conclusion
        st.markdown("### 5. Conclusion")
        st.write(
            "Cognitive constraints limit human prediction in broad, ambiguous domains. SATs offer tools to manage biases, but their success relies on thoughtful application, robust training, and organizational support. Further empirical research is needed to evaluate real-world impact."
        )
        # References
        st.markdown("**References**")
        st.markdown(
            """
            - Chang, W., Berdini, A., & Tetlock, P. (2018). *Intelligence and National Security*.  
            - Cosmides, L., & Tooby, J. (1996). *Cognition*, 58(1), 1–73.  
            - Dhami, M. K., Careless, J., & Manders, C. (2015). Evaluation of ACH Method.  
            - Gigerenzer, G., & Hoffrage, U. (1995). *Psychological Review*, 102(4), 684–704.  
            - Heuer, R. J. (1999). *Psychology of Intelligence Analysis*.  
            - Heuer, R. J., & Pherson, R. H. (2010). *Structured Analytic Techniques*.  
            - Kahneman, D., & Klein, G. (2009). *American Psychologist*, 64(6), 515–526.  
            - Kahneman, D., & Tversky, A. (1973). *Psychological Review*, 80(4), 237–251.  
            - Klein, G. (2007). Insightful Decision Making.  
            - McDowell, C., & Moxley, J. H. (2016). *Journal of Intelligence Analysis*.  
            - Slovic, P., Fischhoff, B., & Lichtenstein, S. (1980). *Societal Risk Assessment*.  
            - Tetlock, P. E. (2005). *Expert Political Judgment*.  
            - Tetlock, P. E., & Gardner, D. (2015). *Superforecasting*.  
            - Tversky, A., & Kahneman, D. (1983). *Psychological Review*, 90(4), 293–315.  
            - Zenko, M. (2015). *Red Team: How to Succeed by Thinking Like the Enemy*. New York: Basic Books.
            """,
            unsafe_allow_html=True,
        )