import React from 'react';

import FaqElement from './faq_element';

const FAQ_CONTENT = [
  {
    summary: 'What is ShadowMail?',
    content: `ShadowMail is a private email forwarding service.  Any email
      sent to a ShadowMail address will be forwarded on to your
      personal email address.`,
  },
  {
    summary: 'Why did you create this service?',
    content: `Have you ever given your email address to a website only to
      start recieving spam?  ShadowMail is our solution, by giving
      each website a different email address you can see which
      website has sold or lost your details.  You may then delete
      that single email address avoiding all spam while keeping
      your email account intact.`,
  },
  {
    summary: 'Does this service cost money?',
    content: `No. This is a service created for personal use instead of
    financial gain.  We have simply decided to open it up to the
    world.`,
  },
  {
    summary: 'Do you read or record emails?',
    content: `No.  We strongly believe in privacy.  Your emails are not saved,
    read, or otherwise processed.  The only thing we do is append a
    delete link to the end.  All of our code is open source and
    we encourage users to check our methodologies.`,
  },
  {
    summary: 'Are there any limits in place?',
    content: `Yes, currently you may only create 3 emails addresses per hour.
    This is limited by both receiving address and IP address.
    We will explore removing or increasing these limits in the future.`,
  },
  {
    summary: 'Do you accept donations?',
    content: `Currently no.  This is something we may consider in the future
    depending on the popularity of the service.  Either way we
    intend for this service to remain free for everyone to use.`,
  },
];

class FaqContainer extends React.Component {
  render = () => (
    <div className="container">
      <div className="row faq-container">
        <div className="offset-by-two eight columns faq-title">
          Frequently Asked Questions
        </div>
      </div>

      {
        FAQ_CONTENT.map(
          (element) => (
            <FaqElement
              key={element.summary}
              summary={element.summary}
              content={element.content}
            />
          ),
        )
      }
    </div>
  )
}


export default FaqContainer;
